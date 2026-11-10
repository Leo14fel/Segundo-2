package com.sinapuml.project.web;

import com.sinapuml.project.domain.document.ProjectDocument;
import jakarta.validation.Valid;
import jakarta.validation.constraints.NotNull;

public record ValidateProjectDocumentRequest(
        @Valid
        @NotNull(message = "document is required")
        ProjectDocument document
) {
}