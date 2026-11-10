package com.sinapuml.assistant.vision;

public interface UmlClassRegionDetector {
    UmlClassRegionDetection detect(VisionNormalizedImage image, int expectedClassCount);
}
