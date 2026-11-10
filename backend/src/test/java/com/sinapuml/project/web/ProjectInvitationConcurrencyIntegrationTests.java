package com.sinapuml.project.web;

import com.sinapuml.auth.persistence.UserEntity;
import com.sinapuml.auth.persistence.UserRepository;
import com.sinapuml.project.application.ProjectInvitationConflictException;
import com.sinapuml.project.application.ProjectInvitationService;
import com.sinapuml.project.application.ProjectInvitationView;
import com.sinapuml.project.application.ProjectService;
import com.sinapuml.project.domain.Project;
import com.sinapuml.project.persistence.ProjectInvitationRepository;
import com.sinapuml.project.persistence.ProjectInvitationStatus;
import com.sinapuml.project.persistence.ProjectMembershipRepository;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.time.Instant;
import java.util.List;
import java.util.UUID;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

@SpringBootTest(properties = {
        "spring.mongodb.database=sinapuml_cu31_invitation_race_test"
})
class ProjectInvitationConcurrencyIntegrationTests {

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private ProjectService projectService;

    @Autowired
    private ProjectInvitationService invitationService;

    @Autowired
    private ProjectInvitationRepository invitationRepository;

    @Autowired
    private ProjectMembershipRepository membershipRepository;

    @Test
    void concurrentInvitesCreateOnlyOnePendingInvitation() throws Exception {
        UUID ownerId = UUID.randomUUID();
        saveUser(ownerId, "Race Owner");
        Project project = projectService.create(ownerId, "Race invite");
        String targetEmail = "race-target-" + UUID.randomUUID() + "@sinapuml.test";

        List<String> outcomes = runConcurrently(
                () -> inviteOutcome(ownerId, project.id(), targetEmail),
                () -> inviteOutcome(ownerId, project.id(), targetEmail)
        );

        assertTrue(outcomes.contains("OK"));
        assertTrue(outcomes.contains("INVITATION_ALREADY_PENDING"));

        assertEquals(
                1,
                invitationRepository
                        .findAllByProjectIdAndStatusOrderByCreatedAtAsc(
                                project.id(),
                                ProjectInvitationStatus.PENDING
                        )
                        .size()
        );
    }

    @Test
    void concurrentAcceptCreatesExactlyOneMembership() throws Exception {
        UUID ownerId = UUID.randomUUID();
        UUID editorId = UUID.randomUUID();
        saveUser(ownerId, "Accept Owner");
        UserEntity editor = saveUser(editorId, "Accept Editor");
        Project project = projectService.create(ownerId, "Race accept");

        ProjectInvitationView invitation =
                invitationService.invite(
                        ownerId,
                        project.id(),
                        editor.getEmail()
                );

        List<String> outcomes = runConcurrently(
                () -> acceptOutcome(editorId, invitation.id()),
                () -> acceptOutcome(editorId, invitation.id())
        );

        assertTrue(outcomes.contains("OK"));
        assertTrue(outcomes.contains("INVITATION_NOT_PENDING"));

        assertEquals(
                1,
                membershipRepository
                        .findAllByProjectIdOrderByCreatedAtAsc(project.id())
                        .stream()
                        .filter(membership -> membership.getUserId().equals(editorId))
                        .count()
        );
    }

    private UserEntity saveUser(UUID id, String displayName) {
        return userRepository.save(
                new UserEntity(
                        id,
                        displayName,
                        "cu31-race-" + id + "@sinapuml.test",
                        "unused",
                        Instant.now()
                )
        );
    }

    private String inviteOutcome(UUID ownerId, UUID projectId, String email) {
        try {
            invitationService.invite(ownerId, projectId, email);
            return "OK";
        } catch (ProjectInvitationConflictException exception) {
            return exception.getCode();
        }
    }

    private String acceptOutcome(UUID userId, UUID invitationId) {
        try {
            invitationService.accept(userId, invitationId);
            return "OK";
        } catch (ProjectInvitationConflictException exception) {
            return exception.getCode();
        }
    }

    private List<String> runConcurrently(
            java.util.concurrent.Callable<String> first,
            java.util.concurrent.Callable<String> second
    ) throws Exception {
        ExecutorService executor = Executors.newFixedThreadPool(2);
        CountDownLatch start = new CountDownLatch(1);

        try {
            Future<String> a = executor.submit(() -> {
                start.await();
                return first.call();
            });
            Future<String> b = executor.submit(() -> {
                start.await();
                return second.call();
            });

            start.countDown();
            return List.of(a.get(), b.get());
        } finally {
            executor.shutdownNow();
        }
    }
}
