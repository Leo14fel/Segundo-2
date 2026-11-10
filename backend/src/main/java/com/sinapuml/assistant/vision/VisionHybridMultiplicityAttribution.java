package com.sinapuml.assistant.vision;

public record VisionHybridMultiplicityAttribution(
        String edgeId,
        VisionHybridEndpoint endpoint,
        String owner,
        Double confidence
) {
}
