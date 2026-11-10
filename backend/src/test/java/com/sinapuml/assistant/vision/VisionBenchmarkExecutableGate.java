package com.sinapuml.assistant.vision;

import com.sinapuml.assistant.AssistantPlanNormalizer;
import com.sinapuml.assistant.AssistantSemanticPlan;
import com.sinapuml.assistant.UmlAssistantCommandResolver;
import com.sinapuml.collaboration.application.ProjectCommandExecutor;
import com.sinapuml.collaboration.protocol.UmlCommandPayload;
import com.sinapuml.project.domain.document.ProjectDocument;
import com.sinapuml.project.validation.ProjectDocumentValidator;

final class VisionBenchmarkExecutableGate {

    private final UmlAssistantCommandResolver commandResolver =
            new UmlAssistantCommandResolver(
                    new ProjectCommandExecutor(),
                    new AssistantPlanNormalizer()
            );
    private final ProjectDocumentValidator documentValidator =
            new ProjectDocumentValidator();

    Result evaluate(AssistantSemanticPlan plan, ProjectDocument document) {
        try {
            UmlCommandPayload batch = commandResolver.resolve(plan, document);
            ProjectDocument preview = commandResolver.preview(document, batch);
            documentValidator.validate(preview);
            return new Result(true, "");
        } catch (Exception exception) {
            return new Result(
                    false,
                    exception.getClass().getSimpleName() + ": " + exception.getMessage()
            );
        }
    }

    record Result(boolean accepted, String detail) {
    }
}
