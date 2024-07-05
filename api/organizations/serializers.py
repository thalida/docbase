from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

from .models import Workspace


class WorkspaceSerializer(serializers.ModelSerializer):
    is_owner = serializers.SerializerMethodField()
    is_default = serializers.SerializerMethodField()
    databases = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    owner = serializers.PrimaryKeyRelatedField(read_only=True)

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

    def _set_default_workspace(self, instance):
        request_data = self.context["request"].data
        if request_data.get("is_default", False):
            user = self.context["request"].user
            user.default_workspace = instance
            user.save()

    def create(self, validated_data):
        validated_data["owner"] = self.context["request"].user
        validated_data["created_by"] = self.context["request"].user
        validated_data["updated_by"] = self.context["request"].user

        instance = super().create(validated_data)
        self._set_default_workspace(instance)

        return instance

    def update(self, instance, validated_data):
        validated_data["updated_by"] = self.context["request"].user

        instance = super().update(instance, validated_data)
        self._set_default_workspace(instance)

        return instance
