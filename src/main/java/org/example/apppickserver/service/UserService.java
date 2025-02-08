package org.example.apppickserver.service;

import org.example.apppickserver.model.UserEntity;
import org.example.apppickserver.repository.UserRepository;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.Map;
import java.util.Optional;

@Service
public class UserService {
    private final UserRepository userRepository;

    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    // 회원가입 (실패 시 JSON 메시지 반환)
    public ResponseEntity<?> register(String userID, String password) {
        if (userRepository.findByUserID(userID).isPresent()) {
            return createErrorResponse("이미 존재하는 사용자ID입니다.");
        }
        UserEntity user = new UserEntity();
        user.setUserID(userID);
        user.setPassword(password);
        UserEntity savedUser = userRepository.save(user);
        return ResponseEntity.ok(savedUser); // 성공 시 기존 UserEntity 반환
    }

    // 로그인 (실패 시 JSON 메시지 반환)
    public ResponseEntity<?> login(String userID, String password) {
        Optional<UserEntity> userOptional = userRepository.findByUserID(userID);
        if (userOptional.isEmpty() || !userOptional.get().getPassword().equals(password)) {
            return createErrorResponse("잘못된 사용자ID 또는 비밀번호입니다.");
        }
        return ResponseEntity.ok(userOptional.get());
    }

    // 에러 응답 생성 (JSON 형식)
    private ResponseEntity<Map<String, Object>> createErrorResponse(String errorMessage) {
        Map<String, Object> response = new HashMap<>();
        response.put("success", false);
        response.put("error", errorMessage);
        return ResponseEntity.badRequest().body(response);
    }
}
