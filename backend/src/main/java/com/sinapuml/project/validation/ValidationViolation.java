package com.sinapuml.project.validation;

public record ValidationViolation(
        String field,
        String code,
        String message
) {
}