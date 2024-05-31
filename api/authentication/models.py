import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(blank=False, max_length=254, verbose_name="email address")

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"

    @property
    def display_name(self) -> str:
        return self.get_full_name() or self.email

    @property
    def initials(self) -> str:
        return "".join(list(map(lambda name: name[0].upper(), self.display_name.split(" "))))

    def __str__(self):
        return f"{self.display_name} ({self.email})"

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)
        self.username = self.email

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

        user_workspaces = self.workspaces.all()
        if not user_workspaces.exists():
            self.create_workspace(name="Personal Workspace")

    def create_workspace(self, name: str):
        from organizations.models import Workspace, WorkspaceMembership

        workspace = Workspace.objects.create(name=name)
        WorkspaceMembership.objects.create(workspace=workspace, user=self)
        return workspace
