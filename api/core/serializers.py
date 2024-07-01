from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field, PolymorphicProxySerializer

from .models import (
    BooleanFieldConfig,
    ChecklistFieldConfig,
    ChoiceFieldConfig,
    ChoiceFieldOption,
    DateFieldConfig,
    FieldResponse,
    FileFieldConfig,
    NumberFieldConfig,
    Page,
    RelationFieldConfig,
    TextFieldConfig,
    Database,
    View,
    Field,
)


class BooleanFieldConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = BooleanFieldConfig
        fields = [
            "display_format",
            "display_icon",
        ]


class ChecklistFieldConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChecklistFieldConfig
        fields = [
            "display_format",
            "status_format",
        ]


class ChoiceFieldOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChoiceFieldOption
        fields = [
            "id",
            "value",
            "label",
        ]


class ChoiceFieldConfigSerializer(serializers.ModelSerializer):
    options = ChoiceFieldOptionSerializer(many=True)

    class Meta:
        model = ChoiceFieldConfig
        fields = [
            "display_format",
            "is_multi_select",
            "options",
        ]


class DateFieldConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = DateFieldConfig
        fields = [
            "display_format",
        ]


class FileFieldConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileFieldConfig
        fields = [
            "supported_file_types",
            "allow_multiple",
        ]


class NumberFieldConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = NumberFieldConfig
        fields = [
            "display_format",
        ]


class RelationFieldConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelationFieldConfig
        fields = [
            "source_field",
            "related_field",
        ]


class TextFieldConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextFieldConfig
        fields = [
            "display_format",
        ]


class FieldSerializer(serializers.ModelSerializer):
    created_by = serializers.UUIDField(read_only=True)
    updated_by = serializers.UUIDField(read_only=True)
    config = serializers.SerializerMethodField(method_name="get_field_config")

    @extend_schema_field(
        PolymorphicProxySerializer(
            component_name="FieldConfig",
            serializers={
                Field.FieldType.BOOLEAN.value: BooleanFieldConfigSerializer,
                Field.FieldType.CHECKLIST.value: ChecklistFieldConfigSerializer,
                Field.FieldType.CHOICE.value: ChoiceFieldConfigSerializer,
                Field.FieldType.DATE.value: DateFieldConfigSerializer,
                Field.FieldType.FILE.value: FileFieldConfigSerializer,
                Field.FieldType.NUMBER.value: NumberFieldConfigSerializer,
                Field.FieldType.RELATION.value: RelationFieldConfigSerializer,
                Field.FieldType.TEXT.value: TextFieldConfigSerializer,
            },
            resource_type_field_name="field_type",
        ),
    )
    def get_field_config(self, obj):
        config_serializer_map = {
            Field.FieldType.BOOLEAN: BooleanFieldConfigSerializer,
            Field.FieldType.CHECKLIST: ChecklistFieldConfigSerializer,
            Field.FieldType.CHOICE: ChoiceFieldConfigSerializer,
            Field.FieldType.DATE: DateFieldConfigSerializer,
            Field.FieldType.FILE: FileFieldConfigSerializer,
            Field.FieldType.NUMBER: NumberFieldConfigSerializer,
            Field.FieldType.RELATION: RelationFieldConfigSerializer,
            Field.FieldType.TEXT: TextFieldConfigSerializer,
        }

        config_serializer = config_serializer_map[obj.field_type]
        return config_serializer(obj.config, context=self.context).data

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


class FieldResponseMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldResponse
        fields = [
            "data",
        ]


class FieldWithResponseSerializer(FieldSerializer):
    response = serializers.SerializerMethodField(method_name="get_field_response")

    @extend_schema_field(FieldResponseMinimalSerializer)
    def get_field_response(self, obj):
        page = self.context.get("internal_meta", {}).get("page")
        response = FieldResponse.objects.filter(page=page, field=obj).first()
        return FieldResponseMinimalSerializer(response).data

    class Meta:
        model = Field
        fields = FieldSerializer.Meta.fields + ["response"]


class PageSerializer(serializers.ModelSerializer):
    created_by = serializers.UUIDField(read_only=True)
    updated_by = serializers.UUIDField(read_only=True)
    fields = serializers.SerializerMethodField(method_name="get_page_fields")

    @extend_schema_field(FieldWithResponseSerializer(many=True))
    def get_page_fields(self, obj):
        fields = obj.view.fields.all()
        fields_order = obj.view.fields_order
        if len(fields_order) > 0:
            fields = sorted(fields, key=lambda x: fields_order.index(x["id"]))

        context = {
            **self.context,
            "internal_meta": {
                **self.context.get("internal_meta", {}),
                "page": obj,
            },
        }
        return FieldWithResponseSerializer(fields, many=True, context=context).data

    class Meta:
        model = Page
        fields = [
            "id",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
            "database",
            "title",
            "content",
            "attachments",
            "fields",
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
