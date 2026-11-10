package com.sinapuml.assistant.vision;

public record VisionHybridEdgeAnnotation(
        String edgeId,
        String type,
        String markerAt,
        VisionMultiplicityProposal multiplicityA,
        VisionMultiplicityProposal multiplicityB,
        String evidenceLabel,
        Double confidence
) {
}
