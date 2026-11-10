package com.sinapuml.projectassistant.persistence;
import java.util.*;
public interface ProjectAiRequestWriteAccess { Optional<ProjectAiMessageEntity> lockRequest(UUID project, UUID request); }
