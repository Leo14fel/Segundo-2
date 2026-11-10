package com.sinapuml.assistant.vision;

import com.sinapuml.assistant.AssistantActionType;
import com.sinapuml.assistant.AssistantAttributePlan;
import com.sinapuml.assistant.AssistantPlanAction;
import com.sinapuml.assistant.AssistantSemanticPlan;
import com.sinapuml.assistant.AssistantTypeSource;
import com.sinapuml.project.domain.document.ProjectDocument;
import com.sinapuml.project.domain.document.UmlDataType;
import com.sinapuml.project.domain.document.UmlVisibility;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class VisionBenchmarkExecutableGateTests {

    private final VisionBenchmarkExecutableGate gate = new VisionBenchmarkExecutableGate();

    @Test
    void acceptsCanonicalPlan() {
        assertTrue(gate.evaluate(createClass("Cliente", "email"), ProjectDocument.empty()).accepted());
    }

    @Test
    void rejectsInvalidManualClassName() {
        assertFalse(gate.evaluate(createClass("Categoría", "email"), ProjectDocument.empty()).accepted());
    }

    @Test
    void rejectsInvalidManualAttributeName() {
        assertFalse(gate.evaluate(createClass("Libro", "añoPublicacion"), ProjectDocument.empty()).accepted());
    }

    private AssistantSemanticPlan createClass(String className, String attributeName) {
        return new AssistantSemanticPlan(
                "test",
                List.of(new AssistantPlanAction(
                        AssistantActionType.CREATE_CLASS,
                        className,
                        null,
                        List.of(new AssistantAttributePlan(
                                attributeName,
                                UmlDataType.STRING,
                                null,
                                UmlVisibility.PRIVATE,
                                true,
                                false,
                                AssistantTypeSource.EXPLICIT
                        )),
                        null,
                        null,
                        null,
                        null,
                        null,
                        null,
                        null,
                        null,
                        null,
                        null,
                        null,
                        null,
                        null,
                        null
                ))
        );
    }
}
