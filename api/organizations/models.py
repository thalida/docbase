from django.db import models

from api.models import BaseModel


class Workspace(BaseModel):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey("authentication.User", on_delete=models.CASCADE, related_name="owned_workspaces")
    members = models.ManyToManyField(
        "authentication.User",
        related_name="workspaces",
        through="WorkspaceMembership",
        through_fields=("workspace", "user"),
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.owner not in self.members.all():
            self.members.add(self.owner)
            self.save()


class WorkspaceMembership(BaseModel):
    workspace = models.ForeignKey("Workspace", on_delete=models.CASCADE, related_name="memberships")
    user = models.ForeignKey("authentication.User", on_delete=models.CASCADE, related_name="workspace_memberships")

    def __str__(self):
        return f"{self.user} in {self.workspace}"

    def delete(self, *args, **kwargs):
        if self.workspace.owner == self.user:
            raise ValueError("Cannot delete owner from workspace")
        return super().delete(*args, **kwargs)


class WorkspaceInvitation(BaseModel):
    class InvitationStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        ACCEPTED = "accepted", "Accepted"
        REJECTED = "rejected", "Rejected"

    workspace = models.ForeignKey("Workspace", on_delete=models.CASCADE, related_name="invitations")
    email = models.EmailField()
    token = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=InvitationStatus.choices, default=InvitationStatus.PENDING)

    def __str__(self):
        return f"{self.email} invited to {self.workspace}"

    def create_token(self):
        from django.utils.crypto import get_random_string

        self.token = get_random_string(length=32)
        return self.token

    def save(self, *args, **kwargs):
        if not self.token:
            self.create_token()

        return super().save(*args, **kwargs)
