package com.sinapuml.assistant;

import com.sinapuml.assistant.tools.AssistantNativeToolPlanner;
import com.sinapuml.collaboration.protocol.UmlCommandPayload;
import com.sinapuml.project.application.ProjectService;
import com.sinapuml.project.domain.Project;
import com.sinapuml.project.domain.document.DiagramLayout;
import com.sinapuml.project.domain.document.ProjectDocument;
import com.sinapuml.project.domain.document.UmlModel;
import com.sinapuml.project.validation.ProjectDocumentValidator;
import org.junit.jupiter.api.Test;

import java.time.Instant;
import java.util.List;
import java.util.Map;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

class AssistantTextVoicePlannerConvergenceTests {

    @Test
    void textAndVoiceUseTheSameNativeToolPlanner() {
        UUID userId = UUID.randomUUID();
        UUID projectId = UUID.randomUUID();
        ProjectDocument document = new ProjectDocument(
                ProjectDocument.CURRENT_SCHEMA_VERSION,
                new UmlModel(List.of(), List.of()),
                new DiagramLayout(Map.of())
        );
        Project project = new Project(projectId, userId, "P", 0L, document, Instant.now(), Instant.now());

        ProjectService projectService = mock(ProjectService.class);
        AssistantNativeToolPlanner planner = mock(AssistantNativeToolPlanner.class);
        UmlAssistantCommandResolver resolver = mock(UmlAssistantCommandResolver.class);
        ProjectDocumentValidator validator = mock(ProjectDocumentValidator.class);

        AssistantSemanticPlan plan = new AssistantSemanticPlan("Crear Animal", List.of());
        UmlCommandPayload batch = UmlCommandPayload.batch("Crear Animal", List.of());
        when(projectService.get(userId, projectId)).thenReturn(project);
        when(planner.plan("crea animal", document)).thenReturn(plan);
        when(resolver.resolve(any(), any())).thenReturn(batch);
        when(resolver.preview(any(), any())).thenReturn(document);

        AssistantPlanService service = new AssistantPlanService(
                projectService, planner, resolver, validator
        );

        AssistantPlanResponse text = service.plan(userId, projectId, "crea animal");
        AssistantPlanResponse voice = service.planVoice(userId, projectId, "crea animal");

        assertEquals("TEXT", text.source());
        assertEquals("VOICE", voice.source());
        assertEquals(text.plan(), voice.plan());
        verify(planner, times(2)).plan("crea animal", document);
    }
}
