import uuid
from django.db import models


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        "authentication.User", on_delete=models.SET_NULL, related_name="%(class)s_created", null=True, blank=True
    )
    updated_by = models.ForeignKey(
        "authentication.User", on_delete=models.SET_NULL, related_name="%(class)s_updated", null=True, blank=True
    )

    class Meta:
        abstract = True
