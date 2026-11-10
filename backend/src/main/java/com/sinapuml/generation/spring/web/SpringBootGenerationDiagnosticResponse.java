package com.sinapuml.generation.spring.web;

import java.util.UUID;

public record SpringBootGenerationDiagnosticResponse(
        String code,
        UUID elementId,
        String path,
        String message
) {
}
