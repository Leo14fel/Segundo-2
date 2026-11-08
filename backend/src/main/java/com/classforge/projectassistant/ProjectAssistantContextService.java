package com.classforge.projectassistant;

import com.classforge.auth.persistence.UserRepository;
import com.classforge.project.access.ProjectAccessRole;
import com.classforge.project.domain.Project;
import com.classforge.project.persistence.ProjectMembershipRepository;
import com.classforge.projectassistant.persistence.ProjectAssistantMessageStore;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.*;

@Service
public class ProjectAssistantContextService {
    private final org.springframework.data.mongodb.core.MongoTemplate mongo;
    private final ProjectMembershipRepository memberships;
    private final UserRepository users;
    private final ProjectAssistantMessageStore messages;

    @org.springframework.beans.factory.annotation.Autowired
    public ProjectAssistantContextService(ProjectMembershipRepository memberships, UserRepository users, ProjectAssistantMessageStore messages, org.springframework.data.mongodb.core.MongoTemplate mongo) {
        this.mongo = mongo;
        this.memberships = memberships; this.users = users; this.messages = messages;
    }

    public ProjectAssistantContextService(ProjectMembershipRepository memberships, UserRepository users, ProjectAssistantMessageStore messages) { this(memberships, users, messages, null); }

    @Transactional(readOnly = true)
    public ProjectAssistantContext build(Project snapshot, UUID excludedRequest) {
        Map<UUID, String> roles = new LinkedHashMap<>();
        roles.put(snapshot.ownerId(), "OWNER");
        memberships.findAllByProjectIdOrderByCreatedAtAsc(snapshot.id()).stream()
                .filter(member -> member.getRole() == ProjectAccessRole.EDITOR)
                .forEach(member -> roles.putIfAbsent(member.getUserId(), "EDITOR"));
        Map<UUID, String> names = new HashMap<>();
        users.findAllById(roles.keySet()).forEach(user -> names.put(user.getId(), user.getDisplayName()));
        var members = roles.entrySet().stream().map(entry -> new ProjectAssistantContext.Member(
                entry.getKey(), names.getOrDefault(entry.getKey(), "Integrante"), entry.getValue())).toList();
        var criteria = org.springframework.data.mongodb.core.query.Criteria.where("projectId").is(snapshot.id()).and("revisionAfter").lte(snapshot.revision());
        var query = org.springframework.data.mongodb.core.query.Query.query(criteria);
        long total = mongo == null ? 0 : mongo.count(query, com.classforge.activity.ProjectActivityEntity.class);
        var activity = mongo == null ? List.<ProjectAssistantContext.ActivityFact>of() : mongo.find(
                query.with(org.springframework.data.domain.Sort.by(org.springframework.data.domain.Sort.Direction.DESC, "revisionAfter")).limit(50),
                com.classforge.activity.ProjectActivityEntity.class).stream().map(entity -> {
                    var a = entity.toActivity();
                    return new ProjectAssistantContext.ActivityFact(a.actorUserId(), a.actorDisplayName(), a.revisionBefore(), a.revisionAfter(), a.description(), a.createdAt());
                }).sorted(java.util.Comparator.comparingLong(ProjectAssistantContext.ActivityFact::revisionAfter)).toList();
        return new ProjectAssistantContext(snapshot.id(), snapshot.name(), snapshot.revision(), snapshot.document(),
                members, messages.recent(snapshot.id(), excludedRequest), activity, total);
    }
}
