package com.sinapuml.generation.spring.api.contract;

import com.sinapuml.generation.spring.application.SpringBootGenerationMode;
import java.util.List;

public record SpringApiContract(
        SpringBootGenerationMode mode,
        List<SpringApiContractOperation> operations
) {
    public SpringApiContract {
        operations = List.copyOf(operations == null ? List.of() : operations);
    }

    public boolean authEnabled() {
        return mode == SpringBootGenerationMode.AUTH_INFORMATION_SYSTEM;
    }
}
