package com.sinapuml.assistant;

public record AssistantRuntimeStatus(
        String name,
        boolean available,
        String state,
        long latencyMs,
        String message
) {
}