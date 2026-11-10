package com.sinapuml.activity;

import java.util.UUID;

public record ActivityChange(ActivityOperationType operationType, UUID elementId, String description) { }
