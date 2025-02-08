package org.example.apppickserver.model;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.RequiredArgsConstructor;
import lombok.Setter;

import java.time.LocalDateTime;

@Entity
@Getter
@Setter
@RequiredArgsConstructor
@Table(name = "board")
public class BoardEntity {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String userID;

    @Column(nullable = false)
    private String title;

    private String mainCategory;
    private String criteria;
    private int star;
    private String content;

    // 생성 시간
    private LocalDateTime createdAt;

    // 업데이트 시간(필요 시)
    private LocalDateTime updatedAt;

    // Insert 전 자동 설정
    @PrePersist
    public void prePersist() {
        this.createdAt = LocalDateTime.now();
        this.updatedAt = LocalDateTime.now();
    }

    // Update 전 자동 설정
    @PreUpdate
    public void preUpdate() {
        this.updatedAt = LocalDateTime.now();
    }
}
