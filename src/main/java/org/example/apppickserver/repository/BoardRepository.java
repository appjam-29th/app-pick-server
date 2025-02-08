package org.example.apppickserver.repository;

import org.example.apppickserver.model.BoardEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface BoardRepository extends JpaRepository<BoardEntity, Long> {
    // createdAt 기준 내림차순 정렬
    List<BoardEntity> findAllByOrderByCreatedAtDesc();

    List<BoardEntity> findByMainCategoryIn(List<String> mainCategories);

    List<BoardEntity> findByCriteriaIn(List<String> criteriaList);

    List<BoardEntity> findByMainCategoryInAndCriteriaIn(List<String> mainCategories, List<String> criteriaList);
}
