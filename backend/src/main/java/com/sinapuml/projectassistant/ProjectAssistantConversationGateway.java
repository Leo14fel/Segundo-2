package com.sinapuml.projectassistant;

public interface ProjectAssistantConversationGateway {
    AssistantConversationResponse respond(ProjectAssistantContext context, String userMessage, AssistantMode mode);
}
