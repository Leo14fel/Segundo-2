package com.sinapuml.assistant;

public interface SpeechToTextGateway {

    String transcribe(
            byte[] wavAudio,
            String filename
    );
}