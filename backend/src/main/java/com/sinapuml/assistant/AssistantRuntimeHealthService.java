package com.sinapuml.assistant;

import com.sinapuml.project.application.ProjectService;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.time.Instant;
import java.util.UUID;

@Service
public class AssistantRuntimeHealthService {

    private final ProjectService projectService;
    private final AssistantRuntimeProbe runtimeProbe;
    private final AssistantVisionRuntimeProbe visionRuntimeProbe;
    private final String textProvider;
    private final String visionProvider;
    private final String llamaUrl;
    private final String whisperUrl;
    private final String visionUrl;
    private final String visionModel;
    private final String bedrockRegion;
    private final String bedrockTextModel;
    private final String bedrockVisionModel;

    public AssistantRuntimeHealthService(
            ProjectService projectService,
            AssistantRuntimeProbe runtimeProbe,
            AssistantVisionRuntimeProbe visionRuntimeProbe,
            @Value("${sinapuml.assistant.text.provider:llama-cpp}") String textProvider,
            @Value("${sinapuml.assistant.vision.provider:llama-cpp}") String visionProvider,
            @Value("${sinapuml.assistant.llama-url:http://127.0.0.1:8092}") String llamaUrl,
            @Value("${sinapuml.assistant.whisper-url:http://127.0.0.1:8093}") String whisperUrl,
            @Value("${sinapuml.assistant.vision.url:http://127.0.0.1:8094}") String visionUrl,
            @Value("${sinapuml.assistant.vision.model:vision-model}") String visionModel,
            @Value("${sinapuml.assistant.bedrock.region:us-east-1}") String bedrockRegion,
            @Value("${sinapuml.assistant.bedrock.text-model:us.amazon.nova-2-lite-v1:0}") String bedrockTextModel,
            @Value("${sinapuml.assistant.bedrock.vision-model:us.amazon.nova-2-lite-v1:0}") String bedrockVisionModel
    ) {
        this.projectService = projectService;
        this.runtimeProbe = runtimeProbe;
        this.visionRuntimeProbe = visionRuntimeProbe;
        this.textProvider = normalized(textProvider, "llama-cpp");
        this.visionProvider = normalized(visionProvider, "llama-cpp");
        this.llamaUrl = llamaUrl;
        this.whisperUrl = whisperUrl;
        this.visionUrl = visionUrl;
        this.visionModel = visionModel;
        this.bedrockRegion = bedrockRegion;
        this.bedrockTextModel = bedrockTextModel;
        this.bedrockVisionModel = bedrockVisionModel;
    }

    public AssistantRuntimeHealthResponse health(UUID userId, UUID projectId) {
        projectService.get(userId, projectId);

        AssistantRuntimeStatus text = "bedrock".equals(textProvider)
                ? configuredBedrock("bedrock-text", bedrockTextModel)
                : runtimeProbe.probe("llama.cpp", llamaUrl);

        AssistantRuntimeStatus whisper = runtimeProbe.probe("whisper.cpp", whisperUrl);

        AssistantRuntimeStatus vision = "bedrock".equals(visionProvider)
                ? configuredBedrock("bedrock-vision", bedrockVisionModel)
                : visionRuntimeProbe.probe(visionUrl, visionModel);

        return new AssistantRuntimeHealthResponse(
                text.available(),
                text.available() && whisper.available(),
                vision.available(),
                text,
                whisper,
                vision,
                Instant.now()
        );
    }

    private AssistantRuntimeStatus configuredBedrock(String component, String modelId) {
        return new AssistantRuntimeStatus(
                component,
                true,
                "CONFIGURED",
                0,
                modelId + " · " + bedrockRegion + " · IAM/model access se valida en la llamada real"
        );
    }

    private String normalized(String value, String fallback) {
        return value == null || value.isBlank() ? fallback : value.trim().toLowerCase(java.util.Locale.ROOT);
    }
}
