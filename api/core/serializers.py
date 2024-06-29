from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

from authentication.serializers import UserMinimalSerializer

from .models import Database, View, Field


class FieldSerializer(serializers.ModelSerializer):
    created_by = serializers.UUIDField(read_only=True)
    updated_by = serializers.UUIDField(read_only=True)

    class Meta:
        model = Field
        fields = [
            "id",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
            "database",
            "label",
            "field_type",
            "config",
        ]

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        validated_data["updated_by"] = self.context["request"].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data["updated_by"] = self.context["request"].user
        return super().update(instance, validated_data)


class ViewSerializer(serializers.ModelSerializer):
    created_by = serializers.UUIDField(read_only=True)
    updated_by = serializers.UUIDField(read_only=True)
    fields = serializers.SerializerMethodField(method_name="get_view_fields")

    @extend_schema_field(FieldSerializer(many=True))
    def get_view_fields(self, obj):
        fields = obj.fields
        if len(obj.fields_order) > 0:
            fields = sorted(fields, key=lambda x: obj.fields_order.index(x["id"]))

        return FieldSerializer(fields, many=True).data

    class Meta:
        model = View
        fields = [
            "id",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
            "database",
            "label",
            "description",
            "view_type",
            "fields",
            "sort_by",
            "filter_by",
        ]

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        validated_data["updated_by"] = self.context["request"].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data["updated_by"] = self.context["request"].user
        return super().update(instance, validated_data)


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
            "views",
        ]

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        validated_data["updated_by"] = self.context["request"].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data["updated_by"] = self.context["request"].user
        return super().update(instance, validated_data)
