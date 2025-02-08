package org.example.apppickserver.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.RequiredArgsConstructor;

@Data
@RequiredArgsConstructor
@AllArgsConstructor
public class BoardPatchRequest {
    private String title;
    private String mainCategory;
    private String criteria;
    private String content;
    private Integer star;
}