package com.sinapuml.assistant;

import com.sinapuml.collaboration.application.ProjectCommandExecutor;
import com.sinapuml.collaboration.protocol.UmlCommandPayload;
import com.sinapuml.project.domain.document.ProjectDocument;
import com.sinapuml.project.domain.document.UmlClass;
import com.sinapuml.project.domain.document.UmlModel;
import com.sinapuml.project.domain.document.DiagramLayout;
import com.sinapuml.project.domain.document.UmlRelationship;
import com.sinapuml.project.domain.document.UmlRelationshipType;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNull;

class UmlAssistantMultiplicityRegressionTests {

    private final UmlAssistantCommandResolver resolver =
            new UmlAssistantCommandResolver(
                    new ProjectCommandExecutor(),
                    new AssistantPlanNormalizer()
            );

    @Test
    void minusOneUpperBecomesUnlimitedMultiplicityWithoutUnboxingNull() {
        UmlClass animal =
                new UmlClass(
                        UUID.randomUUID(),
                        "Animal",
                        List.of()
                );

        UmlClass veterinario =
                new UmlClass(
                        UUID.randomUUID(),
                        "Veterinario",
                        List.of()
                );

        ProjectDocument document =
                new ProjectDocument(
                        ProjectDocument.CURRENT_SCHEMA_VERSION,
                        new UmlModel(
                                List.of(
                                        animal,
                                        veterinario
                                ),
                                List.of()
                        ),
                        DiagramLayout.empty()
                );

        AssistantPlanAction action =
                new AssistantPlanAction(
                        AssistantActionType.CREATE_RELATIONSHIP,
                        null,
                        null,
                        List.of(),
                        null,
                        null,
                        null,
                        null,
                        null,
                        null,
                        null,
                        "Veterinario",
                        "Animal",
                        UmlRelationshipType.ASSOCIATION,
                        1,
                        1,
                        0,
                        -1
                );

        UmlCommandPayload batch =
                resolver.resolve(
                        new AssistantSemanticPlan(
                                "Relacionar Veterinario con muchos Animal",
                                List.of(
                                        action
                                )
                        ),
                        document
                );

        ProjectDocument preview =
                resolver.preview(
                        document,
                        batch
                );

        UmlRelationship relationship =
                preview.umlModel()
                        .relationships()
                        .getFirst();

        assertEquals(
                1,
                relationship.sourceMultiplicity()
                        .lower()
        );

        assertEquals(
                1,
                relationship.sourceMultiplicity()
                        .upper()
        );

        assertEquals(
                0,
                relationship.targetMultiplicity()
                        .lower()
        );

        assertNull(
                relationship.targetMultiplicity()
                        .upper()
        );
    }

    @Test
    void omittedMultiplicityStillDefaultsToOneToOne() {
        UmlClass animal =
                new UmlClass(
                        UUID.randomUUID(),
                        "Animal",
                        List.of()
                );

        UmlClass veterinario =
                new UmlClass(
                        UUID.randomUUID(),
                        "Veterinario",
                        List.of()
                );

        ProjectDocument document =
                new ProjectDocument(
                        ProjectDocument.CURRENT_SCHEMA_VERSION,
                        new UmlModel(
                                List.of(
                                        animal,
                                        veterinario
                                ),
                                List.of()
                        ),
                        DiagramLayout.empty()
                );

        AssistantPlanAction action =
                new AssistantPlanAction(
                        AssistantActionType.CREATE_RELATIONSHIP,
                        null,
                        null,
                        List.of(),
                        null,
                        null,
                        null,
                        null,
                        null,
                        null,
                        null,
                        "Animal",
                        "Veterinario",
                        UmlRelationshipType.ASSOCIATION,
                        null,
                        null,
                        null,
                        null
                );

        UmlCommandPayload batch =
                resolver.resolve(
                        new AssistantSemanticPlan(
                                "Conecta Animal con Veterinario",
                                List.of(
                                        action
                                )
                        ),
                        document
                );

        ProjectDocument preview =
                resolver.preview(
                        document,
                        batch
                );

        UmlRelationship relationship =
                preview.umlModel()
                        .relationships()
                        .getFirst();

        assertEquals(
                1,
                relationship.sourceMultiplicity()
                        .lower()
        );

        assertEquals(
                1,
                relationship.sourceMultiplicity()
                        .upper()
        );

        assertEquals(
                1,
                relationship.targetMultiplicity()
                        .lower()
        );

        assertEquals(
                1,
                relationship.targetMultiplicity()
                        .upper()
        );
    }
}