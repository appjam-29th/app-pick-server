package org.example.apppickserver.controller;

import org.example.apppickserver.dto.BoardPatchRequest;
import org.example.apppickserver.model.BoardEntity;
import org.example.apppickserver.service.BoardService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.*;

@RestController
@RequestMapping("/api/board")
public class BoardController {
    private final BoardService boardService;

    public BoardController(BoardService boardService) {
        this.boardService = boardService;
    }

    // 전체 조회
    @GetMapping
    public ResponseEntity<List<BoardEntity>> getAllBoards() {
        return ResponseEntity.ok(boardService.getAllBoards());
    }

    // 등록
    @PostMapping
    public ResponseEntity<BoardEntity> createBoard(@RequestBody BoardEntity req) {
        return ResponseEntity.ok(
                boardService.createBoard(
                        req.getUserID(),
                        req.getTitle(),
                        req.getMainCategory(),
                        req.getCriteria(),
                        req.getStar(),
                        req.getContent()
                )
        );
    }

    // 예: /api/board/filter?mainCategory=홈,디자인&criteria=편리함,낮은 접근성
    /**
     * 예: GET /api/board/filter?mainCategory=홈,쇼핑&criteria=편리함,낮은 접근성
     * => mainCategoryList=["홈","쇼핑"], criteriaList=["편리함","낮은 접근성"]
     * => DB에 "mainCategory"="홈/쇼핑" 이고 "criteria"="편리함/낮은 접근성" 인 데이터만 추출
     */
    /**
     * 예: GET /api/board/filter?mainCategory=홈,디자인&criteria=편리함,유용성
     * => mainCatList=["홈","디자인"], criteriaList=["편리함","유용성"]
     * => DB에서는 mainCategory="홈/디자인", criteria="편리함/유용성" 인 레코드만 반환
     * (둘 중 하나만 일치해도 안됨, 둘 다 정확히 일치해야 함)
     */
    @GetMapping("/filter")
    public ResponseEntity<List<BoardEntity>> filterBoard(
            @RequestParam(required = false) String mainCategory,
            @RequestParam(required = false) String criteria
    ) {
        // 콤마로 분리 -> 리스트화
        List<String> mainCatList = (mainCategory == null || mainCategory.isEmpty())
                ? Collections.emptyList()
                : Arrays.asList(mainCategory.split(","));
        List<String> criteriaList = (criteria == null || criteria.isEmpty())
                ? Collections.emptyList()
                : Arrays.asList(criteria.split(","));

        List<BoardEntity> result = boardService.filterExactSet(mainCatList, criteriaList);
        return ResponseEntity.ok(result);
    }

    // 단일 게시글 조회 (id로 조회)
    @GetMapping("/{id}")
    public ResponseEntity<BoardEntity> getBoardById(@PathVariable Long id) {
        BoardEntity board = boardService.getBoardById(id);
        return ResponseEntity.ok(board);
    }


    // 일부 수정 (PATCH)
    // userID가 다르면 "수정 권한이 없습니다." 메시지 반환
    @PatchMapping("/{id}")
    public ResponseEntity<?> patchBoard(
            @PathVariable Long id,
            @RequestParam String userID, // 쿼리 파라미터로 userID 전달
            @RequestBody BoardPatchRequest patchRequest
    ) {
        try {
            BoardEntity updated = boardService.patchBoard(id, userID, patchRequest);
            return ResponseEntity.ok(updated);
        } catch (RuntimeException e) {
            // JSON 형태로 오류 메시지 반환
            Map<String, String> errorResponse = new HashMap<>();
            errorResponse.put("message", e.getMessage()); // "수정 권한이 없습니다." 등
            return ResponseEntity.badRequest().body(errorResponse);
        }
    }
}
