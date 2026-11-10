package com.sinapuml.assistant.vision;

public record VisionHybridMultiplicityTranscription(
        String edgeId,
        VisionHybridEndpoint endpoint,
        String rawLabel,
        Double confidence
) {
}
