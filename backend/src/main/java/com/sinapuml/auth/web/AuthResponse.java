package com.sinapuml.auth.web;

public record AuthResponse(
        String accessToken,
        String tokenType,
        long expiresInSeconds,
        UserResponse user
) {
}