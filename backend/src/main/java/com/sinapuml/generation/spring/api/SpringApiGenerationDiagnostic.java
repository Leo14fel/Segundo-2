package com.sinapuml.generation.spring.api;

import java.util.UUID;

public record SpringApiGenerationDiagnostic(
        SpringApiGenerationDiagnosticCode code,
        UUID elementId,
        String path,
        String message
) { }
