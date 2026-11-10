package com.sinapuml.assistant;

import com.sinapuml.project.domain.document.UmlDataType;
import com.sinapuml.project.domain.document.UmlVisibility;

public record AssistantAttributePlan(
        String name,
        UmlDataType dataType,
        String customTypeName,
        UmlVisibility visibility,
        Boolean nullable,
        Boolean identifier,
        AssistantTypeSource typeSource
) {
}