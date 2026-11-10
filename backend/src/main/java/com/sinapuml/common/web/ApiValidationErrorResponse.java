package com.sinapuml.common.web;

import com.sinapuml.project.validation.ValidationViolation;

import java.util.List;

public record ApiValidationErrorResponse(
        String error,
        String message,
        List<ValidationViolation> violations
) {
}