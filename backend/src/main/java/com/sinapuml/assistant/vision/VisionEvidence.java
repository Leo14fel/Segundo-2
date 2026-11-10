package com.sinapuml.assistant.vision;

public record VisionEvidence(
        String label,
        Double confidence,
        Integer x,
        Integer y,
        Integer width,
        Integer height
) {
}
