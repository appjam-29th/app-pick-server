package org.example.apppickserver.controller;

import org.example.apppickserver.service.UserService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api")
public class AuthController {
    private final UserService userService;

    public AuthController(UserService userService) {
        this.userService = userService;
    }

    // 회원가입 (실패 시 JSON 메시지 반환)
    @PostMapping("/register")
    public ResponseEntity<?> register(@RequestBody Map<String, String> req) {
        String userID = req.get("userID");
        String password = req.get("password");
        return userService.register(userID, password);
    }

    // 로그인 (성공 시 UserEntity 반환, 실패 시 JSON 메시지 반환)
    @PostMapping("/login")
    public ResponseEntity<?> login(@RequestBody Map<String, String> req) {
        String userID = req.get("userID");
        String password = req.get("password");
        return userService.login(userID, password);
    }
}
