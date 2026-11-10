package com.sinapuml.assistant;

import com.sinapuml.collaboration.protocol.UmlCommandPayload;

public record AssistantPlanResponse(
        String source,
        String transcript,
        long baseRevision,
        String summary,
        AssistantSemanticPlan plan,
        UmlCommandPayload command
) {
}