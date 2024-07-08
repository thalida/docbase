from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "display_name",
            "initials",
            "avatar",
        ]


class MyUserSerializer(UserSerializer):
    invitations = serializers.SerializerMethodField()

    @extend_schema_field(serializers.ListField(child=serializers.UUIDField()))
    def get_invitations(self, obj):
        from organizations.models import WorkspaceInvitation

        invitations = WorkspaceInvitation.objects.filter(email=obj.email).distinct()
        return [invitation.id for invitation in invitations]

    class Meta:
        model = User
        fields = UserSerializer.Meta.fields + [
            "workspaces",
            "default_workspace",
            "invitations",
        ]
