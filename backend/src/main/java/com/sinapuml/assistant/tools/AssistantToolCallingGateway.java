package com.sinapuml.assistant.tools;

import com.sinapuml.project.domain.document.ProjectDocument;

import java.util.List;

public interface AssistantToolCallingGateway {

    default List<AssistantToolInvocation> call(
            String userText,
            ProjectDocument document,
            AssistantToolCatalog catalog
    ) {
        return call(userText, document, catalog, List.of());
    }

    List<AssistantToolInvocation> call(
            String userText,
            ProjectDocument document,
            AssistantToolCatalog catalog,
            List<AssistantToolConversationTurn> history
    );
}
