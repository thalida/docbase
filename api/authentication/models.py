import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(blank=False, max_length=254, verbose_name="email address")
    avatar = models.URLField(blank=True, null=True)
    default_workspace = models.ForeignKey(
        "organizations.Workspace", on_delete=models.SET_NULL, blank=True, null=True, related_name="default_for_users"
    )

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"

    @property
    def display_name(self) -> str:
        email_first_part = self.email.split("@")[0]
        return self.get_full_name() or email_first_part

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

        has_workspace = self.workspaces.exists()
        if not has_workspace:
            from organizations.models import Workspace

            workspace = Workspace.objects.create(owner=self, name=f"{self.display_name}'s workspace")
            self.workspaces.add(workspace)
            self.default_workspace = workspace
            self.save()
