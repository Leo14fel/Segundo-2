package com.sinapuml.integration.xmi;

public record XmiDiagnostic(
        XmiDiagnosticSeverity severity,
        String code,
        String message
) {
}
