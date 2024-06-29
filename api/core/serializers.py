from rest_framework import serializers

from authentication.serializers import UserMinimalSerializer

from .models import Database


class DatabaseSerializer(serializers.ModelSerializer):
    created_by = UserMinimalSerializer(read_only=True)
    updated_by = UserMinimalSerializer(read_only=True)

    class Meta:
        model = Database
        fields = [
            "id",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
            "workspace",
            "name",
            "description",
            "page_format_string",
        ]

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        validated_data["updated_by"] = self.context["request"].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data["updated_by"] = self.context["request"].user
        return super().update(instance, validated_data)
