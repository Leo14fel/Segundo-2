package com.sinapuml.auth.application;

import com.sinapuml.auth.persistence.UserEntity;
import com.sinapuml.auth.persistence.UserRepository;
import com.sinapuml.auth.security.JwtService;
import com.sinapuml.auth.web.AuthResponse;
import com.sinapuml.auth.web.LoginRequest;
import com.sinapuml.auth.web.RegisterRequest;
import com.sinapuml.auth.web.UserResponse;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.Instant;
import java.util.Locale;
import java.util.UUID;

@Service
public class AuthService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtService jwtService;

    public AuthService(
            UserRepository userRepository,
            PasswordEncoder passwordEncoder,
            JwtService jwtService
    ) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
        this.jwtService = jwtService;
    }

    @Transactional
    public AuthResponse register(RegisterRequest request) {
        String email = normalizeEmail(request.email());

        if (userRepository.existsByEmailIgnoreCase(email)) {
            throw new EmailAlreadyRegisteredException();
        }

        UserEntity user = new UserEntity(
                UUID.randomUUID(),
                request.displayName().trim(),
                email,
                passwordEncoder.encode(request.password()),
                Instant.now()
        );

        UserEntity saved = userRepository.save(user);
        return responseFor(saved);
    }

    @Transactional(readOnly = true)
    public AuthResponse login(LoginRequest request) {
        UserEntity user = userRepository.findByEmailIgnoreCase(normalizeEmail(request.email()))
                .orElseThrow(InvalidCredentialsException::new);

        if (!passwordEncoder.matches(request.password(), user.getPasswordHash())) {
            throw new InvalidCredentialsException();
        }

        return responseFor(user);
    }

    @Transactional(readOnly = true)
    public UserEntity getUser(UUID userId) {
        return userRepository.findById(userId)
                .orElseThrow(InvalidCredentialsException::new);
    }

    private AuthResponse responseFor(UserEntity user) {
        return new AuthResponse(
                jwtService.issue(user),
                "Bearer",
                jwtService.expirationSeconds(),
                UserResponse.from(user)
        );
    }

    private String normalizeEmail(String email) {
        return email.trim().toLowerCase(Locale.ROOT);
    }
}