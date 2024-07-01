from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

from .models import Workspace


class WorkspaceSerializer(serializers.ModelSerializer):
    is_owner = serializers.SerializerMethodField()

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
            "is_owner",
            "databases",
        ]

    @extend_schema_field(serializers.BooleanField())
    def get_is_owner(self, obj):
        return obj.owner == self.context["request"].user

    def create(self, validated_data):
        validated_data["owner"] = self.context["request"].user
        validated_data["created_by"] = self.context["request"].user
        validated_data["updated_by"] = self.context["request"].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data["updated_by"] = self.context["request"].user
        return super().update(instance, validated_data)
