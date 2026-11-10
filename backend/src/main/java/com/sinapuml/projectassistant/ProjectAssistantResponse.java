package com.sinapuml.projectassistant;

public record ProjectAssistantResponse(ProjectAiMessage userMessage, ProjectAiMessage assistantMessage,
                                       long projectRevision) { }
