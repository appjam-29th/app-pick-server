package org.example.apppickserver.model;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;
import org.hibernate.annotations.GenericGenerator;

@Entity
@Getter
@Setter
public class UserEntity {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;  // 정수 PK

    @Column(nullable = false, unique = true)
    private String userID; // 사용자가 입력하는 식별자(중복 방지)

    private String password;
}
