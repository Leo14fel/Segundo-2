package com.sinapuml.projectassistant;

import java.util.List;

public record ProjectAssistantHistory(List<ProjectAiMessage> messages, boolean hasMore) { }
