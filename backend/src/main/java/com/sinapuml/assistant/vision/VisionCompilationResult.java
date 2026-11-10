package com.sinapuml.assistant.vision;

import com.sinapuml.assistant.AssistantSemanticPlan;

import java.util.List;

public record VisionCompilationResult(
        AssistantSemanticPlan plan,
        List<String> warnings,
        double confidence
) {
}
