package com.sinapuml.assistant.tools;

import com.sinapuml.assistant.AssistantSemanticPlan;

import java.util.List;

public record AssistantToolResolution(
        AssistantSemanticPlan plan,
        List<AssistantResolvedReference> references
) {
}
