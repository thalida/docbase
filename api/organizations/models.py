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


class WorkspaceMembership(BaseModel):
    workspace = models.ForeignKey("Workspace", on_delete=models.CASCADE, related_name="memberships")
    user = models.ForeignKey("authentication.User", on_delete=models.CASCADE, related_name="workspace_memberships")

    def __str__(self):
        return f"{self.user} in {self.workspace}"
