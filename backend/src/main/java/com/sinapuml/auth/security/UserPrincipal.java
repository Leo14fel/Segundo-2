package com.sinapuml.auth.security;

import java.util.UUID;

public record UserPrincipal(UUID id, String email) {
}