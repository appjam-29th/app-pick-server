package org.example.apppickserver.controller;

import org.example.apppickserver.model.UserEntity;
import org.example.apppickserver.service.UserService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api")
public class AuthController {
    private final UserService userService;

    public AuthController(UserService userService) {
        this.userService = userService;
    }

    // 회원가입
    @PostMapping("/register")
    public ResponseEntity<UserEntity> register(@RequestBody UserEntity req) {
        return ResponseEntity.ok(userService.register(req.getUserID(), req.getPassword()));
    }

    // 로그인
    @PostMapping("/login")
    public ResponseEntity<UserEntity> login(@RequestBody UserEntity req) {
        return ResponseEntity.ok(userService.login(req.getUserID(), req.getPassword()));
    }
}
