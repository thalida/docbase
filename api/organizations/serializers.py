from rest_framework import serializers

from authentication.serializers import UserMinimalSerializer

from .models import Workspace


class WorkspaceSerializer(serializers.ModelSerializer):
    members = UserMinimalSerializer(many=True, read_only=True)

    class Meta:
        model = Workspace
        fields = [
            "id",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
            "name",
            "owner",
            "members",
        ]
