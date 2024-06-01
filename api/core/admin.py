from typing import Any

from django.contrib import admin
from unfold.admin import ModelAdmin, StackedInline

from core.models import (
    Attachment,
    BooleanFieldConfig,
    ChecklistFieldConfig,
    ChoiceFieldConfig,
    ChoiceFieldOption,
    Database,
    DateFieldConfig,
    Field,
    FieldResponse,
    FileFieldConfig,
    Folder,
    NumberFieldConfig,
    Page,
    RelationFieldConfig,
    TextFieldConfig,
    View,
)


class FieldInline(StackedInline):
    model = Field
    extra = 0
    exclude = ("created_by", "updated_by")

    class Media:
        js = ("core/js/admin_fields.js",)

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        field = super().formfield_for_dbfield(db_field, request, **kwargs)

        if field is None:
            return field

        if db_field.name.endswith("_config"):
            inverse_config_field_map = {value: key for key, value in Field._config_field_map.items()}
            field.widget.attrs["data-config-field-type"] = inverse_config_field_map[db_field.name]

        if db_field.name == "field_type":
            field.widget.attrs["data-config-field-controller"] = True

        return field


@admin.register(Field)
class FieldAdmin(ModelAdmin):
    list_display = ("label", "database", "created_at", "updated_at")
    search_fields = ("label",)
    list_filter = ("database",)
    exclude = ("created_by", "updated_by")

    class Media:
        js = ("core/js/admin_fields.js",)

    def get_form(self, request, obj=None, change=False, **kwargs) -> Any:
        form = super().get_form(request, obj, change, **kwargs)

        form.base_fields["field_type"].widget.attrs["data-config-field-controller"] = True

        inverse_config_field_map = {value: key for key, value in Field._config_field_map.items()}
        for field in form.base_fields:
            if not str(field).endswith("_config"):
                continue

            form.base_fields[field].widget.attrs["data-config-field-type"] = inverse_config_field_map[field]

        return form


@admin.register(BooleanFieldConfig)
class BooleanFieldConfigAdmin(ModelAdmin):
    list_display = ("created_at", "updated_at")
    search_fields = ()
    exclude = ("created_by", "updated_by")


@admin.register(ChecklistFieldConfig)
class ChecklistFieldConfigAdmin(ModelAdmin):
    list_display = ("created_at", "updated_at")
    search_fields = ()
    exclude = ("created_by", "updated_by")


class ChoiceOptionInline(StackedInline):
    model = ChoiceFieldOption
    extra = 0
    exclude = ("created_by", "updated_by")


@admin.register(ChoiceFieldConfig)
class ChoiceFieldConfigAdmin(ModelAdmin):
    list_display = ("created_at", "updated_at")
    search_fields = ()
    exclude = ("created_by", "updated_by")
    inlines = [
        ChoiceOptionInline,
    ]


@admin.register(DateFieldConfig)
class DateFieldConfigAdmin(ModelAdmin):
    list_display = ("created_at", "updated_at")
    search_fields = ()
    exclude = ("created_by", "updated_by")


@admin.register(FileFieldConfig)
class FileFieldConfigAdmin(ModelAdmin):
    list_display = ("created_at", "updated_at")
    search_fields = ()
    exclude = ("created_by", "updated_by")


@admin.register(NumberFieldConfig)
class NumberFieldConfigAdmin(ModelAdmin):
    list_display = ("created_at", "updated_at")
    search_fields = ()
    exclude = ("created_by", "updated_by")


@admin.register(RelationFieldConfig)
class RelationFieldConfigAdmin(ModelAdmin):
    list_display = ("created_at", "updated_at")
    search_fields = ()
    exclude = ("created_by", "updated_by")


@admin.register(TextFieldConfig)
class TextFieldConfigAdmin(ModelAdmin):
    list_display = ("created_at", "updated_at")
    search_fields = ()
    exclude = ("created_by", "updated_by")


class ViewInline(StackedInline):
    model = View
    extra = 0
    exclude = ("created_by", "updated_by")


@admin.register(Database)
class DatabaseAdmin(ModelAdmin):
    list_display = ("name", "workspace", "created_at", "updated_at")
    search_fields = ("name",)
    list_filter = ("workspace",)
    exclude = ("created_by", "updated_by")

    inlines = [
        FieldInline,
    ]


@admin.register(View)
class ViewAdmin(ModelAdmin):
    list_display = ("label", "database", "created_at", "updated_at")
    search_fields = ("label",)
    list_filter = ("database",)
    exclude = ("created_by", "updated_by")


@admin.register(Folder)
class FolderAdmin(ModelAdmin):
    list_display = ("label", "workspace", "created_at", "updated_at")
    search_fields = ("label",)
    list_filter = ("workspace",)
    exclude = ("created_by", "updated_by")


class FieldResponseInline(StackedInline):
    model = FieldResponse
    extra = 0
    exclude = ("created_by", "updated_by")


@admin.register(Page)
class PageAdmin(ModelAdmin):
    list_display = ("title", "database", "created_at", "updated_at")
    search_fields = ("title",)
    list_filter = ("database",)
    exclude = ("created_by", "updated_by")
    inlines = [
        FieldResponseInline,
    ]


@admin.register(Attachment)
class AttachmentAdmin(ModelAdmin):
    list_display = ("file", "created_at", "updated_at")
    exclude = ("created_by", "updated_by")
