package org.example.apppickserver.service;

import org.example.apppickserver.model.UserEntity;
import org.example.apppickserver.repository.UserRepository;
import org.springframework.stereotype.Service;

@Service
public class UserService {
    private final UserRepository userRepository;

    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    // 회원가입
    public UserEntity register(String userID, String password) {
        if (userRepository.findByUserID(userID).isPresent()) {
            throw new RuntimeException("이미 존재하는 사용자ID입니다.");
        }
        UserEntity user = new UserEntity();
        user.setUserID(userID);
        user.setPassword(password);
        return userRepository.save(user);
    }

    // 로그인
    public UserEntity login(String userID, String password) {
        return userRepository.findByUserID(userID)
                .filter(u -> u.getPassword().equals(password))
                .orElseThrow(() -> new RuntimeException("잘못된 사용자ID 또는 비밀번호입니다."));
    }
}
