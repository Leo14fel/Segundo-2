package com.sinapuml.project.persistence;
import java.util.*;
public interface ProjectWriteAccess { Optional<ProjectEntity> acquireWrite(UUID id); }
