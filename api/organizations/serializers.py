from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

from .models import Workspace


class WorkspaceSerializer(serializers.ModelSerializer):
    is_owner = serializers.SerializerMethodField()
    is_default = serializers.SerializerMethodField()

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
            "databases",
            "is_owner",
            "is_default",
        ]

    @extend_schema_field(serializers.BooleanField())
    def get_is_owner(self, obj):
        return obj.owner == self.context["request"].user

    @extend_schema_field(serializers.BooleanField())
    def get_is_default(self, obj):
        user = self.context["request"].user
        return user.default_workspace.id == obj.id if user.default_workspace else False

    def create(self, validated_data):
        validated_data["owner"] = self.context["request"].user
        validated_data["created_by"] = self.context["request"].user
        validated_data["updated_by"] = self.context["request"].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data["updated_by"] = self.context["request"].user
        return super().update(instance, validated_data)
