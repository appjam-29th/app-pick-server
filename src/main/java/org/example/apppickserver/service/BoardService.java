package org.example.apppickserver.service;

import org.example.apppickserver.dto.BoardPatchRequest;
import org.example.apppickserver.model.BoardEntity;
import org.example.apppickserver.repository.BoardRepository;
import org.springframework.stereotype.Service;

import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;

@Service
public class BoardService {
    private final BoardRepository boardRepository;

    public BoardService(BoardRepository boardRepository) {
        this.boardRepository = boardRepository;
    }

    // 전체 조회
    public List<BoardEntity> getAllBoards() {
        return boardRepository.findAllByOrderByCreatedAtDesc();
    }

    // 등록
    public BoardEntity createBoard(String userID, String title, String mainCategory, String criteria, int star, String content) {
        BoardEntity board = new BoardEntity();
        board.setUserID(userID);
        board.setTitle(title);
        board.setMainCategory(mainCategory);
        board.setCriteria(criteria);
        board.setStar(star);
        board.setContent(content);
        return boardRepository.save(board);
    }

    /**
     * DB 엔티티의 mainCategory가 "홈/디자인" 이라면,
     * 쿼리 파라미터가 "?mainCategory=홈,디자인"일 때만 일치로 간주.
     * criteria도 같은 방식.
     */
    public List<BoardEntity> filterExactSet(List<String> mainCatList, List<String> criteriaList) {
        List<BoardEntity> all = boardRepository.findAll();

        // 둘 다 비어있으면 전체 반환
        if ((mainCatList == null || mainCatList.isEmpty())
                && (criteriaList == null || criteriaList.isEmpty())) {
            return all;
        }

        return all.stream()
                .filter(board -> {
                    // DB에 저장된 mainCategory "/" 분리 -> set 변환
                    String[] dbMainArray = (board.getMainCategory() == null)
                            ? new String[0]
                            : board.getMainCategory().split("/");
                    Set<String> dbMainSet = new HashSet<>(Arrays.asList(dbMainArray));

                    // 요청값이 있으면, 크기와 원소가 정확히 동일해야 함
                    if (mainCatList != null && !mainCatList.isEmpty()) {
                        Set<String> queryMainSet = new HashSet<>(mainCatList);

                        // 세트 크기, 원소까지 일치해야 통과
                        if (!queryMainSet.equals(dbMainSet)) {
                            return false;
                        }
                    }

                    // DB에 저장된 criteria "/" 분리 -> set 변환
                    String[] dbCritArray = (board.getCriteria() == null)
                            ? new String[0]
                            : board.getCriteria().split("/");
                    Set<String> dbCritSet = new HashSet<>(Arrays.asList(dbCritArray));

                    if (criteriaList != null && !criteriaList.isEmpty()) {
                        Set<String> queryCritSet = new HashSet<>(criteriaList);
                        if (!queryCritSet.equals(dbCritSet)) {
                            return false;
                        }
                    }

                    return true;
                })
                .collect(Collectors.toList());
    }

    // 단일 게시글 조회
    public BoardEntity getBoardById(Long id) {
        return boardRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("해당 ID의 게시글이 존재하지 않습니다."));
    }

    // PATCH 로직
    public BoardEntity patchBoard(Long id, String userID, BoardPatchRequest patchRequest) {
        BoardEntity board = getBoardById(id);

        // userID 검증
        if (!board.getUserID().equals(userID)) {
            throw new RuntimeException("수정 권한이 없습니다.");
        }

        // null이 아닌 필드만 업데이트
        if (patchRequest.getTitle() != null) {
            board.setTitle(patchRequest.getTitle());
        }
        if (patchRequest.getMainCategory() != null) {
            board.setMainCategory(patchRequest.getMainCategory());
        }
        if (patchRequest.getCriteria() != null) {
            board.setCriteria(patchRequest.getCriteria());
        }
        if (patchRequest.getContent() != null) {
            board.setContent(patchRequest.getContent());
        }
        if (patchRequest.getStar() != null) {
            board.setStar(patchRequest.getStar());
        }

        return boardRepository.save(board);
    }
}