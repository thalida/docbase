from django.contrib import admin
from unfold.admin import ModelAdmin, StackedInline

from core.models import (
    Attachment,
    BooleanFieldConfig,
    ChecklistFieldConfig,
    ChoiceFieldConfig,
    Database,
    DateFieldConfig,
    Field,
    FileFieldConfig,
    Folder,
    NumberFieldConfig,
    Page,
    RelationFieldConfig,
    TextFieldConfig,
    View,
)


class BaseFieldConfigInline(StackedInline):
    extra = 0
    exclude = ("created_by", "updated_by")


class TextFieldConfigInline(BaseFieldConfigInline):
    model = TextFieldConfig


class NumberFieldConfigInline(BaseFieldConfigInline):
    model = NumberFieldConfig


class BooleanFieldConfigInline(BaseFieldConfigInline):
    model = BooleanFieldConfig


class DateFieldConfigInline(BaseFieldConfigInline):
    model = DateFieldConfig


class ChecklistFieldConfigInline(BaseFieldConfigInline):
    model = ChecklistFieldConfig


class ChoiceFieldConfigInline(BaseFieldConfigInline):
    model = ChoiceFieldConfig


class FileFieldConfigInline(BaseFieldConfigInline):
    model = FileFieldConfig


class RelationFieldConfigInline(BaseFieldConfigInline):
    model = RelationFieldConfig


class FieldInline(StackedInline):
    model = Field
    extra = 0
    exclude = ("created_by", "updated_by")
    fields = ("label", "field_type")

    inlines = [
        TextFieldConfigInline,
        NumberFieldConfigInline,
        BooleanFieldConfigInline,
        DateFieldConfigInline,
        ChecklistFieldConfigInline,
        ChoiceFieldConfigInline,
        FileFieldConfigInline,
        RelationFieldConfigInline,
    ]


@admin.register(Field)
class FieldAdmin(ModelAdmin):
    list_display = ("label", "database", "created_at", "updated_at")
    search_fields = ("label",)
    list_filter = ("database",)
    exclude = ("created_by", "updated_by")

    inlines = [
        TextFieldConfigInline,
        NumberFieldConfigInline,
        BooleanFieldConfigInline,
        DateFieldConfigInline,
        ChecklistFieldConfigInline,
        ChoiceFieldConfigInline,
    ]


@admin.register(TextFieldConfig)
class TextFieldConfigAdmin(ModelAdmin):
    list_display = ("field", "created_at", "updated_at")
    search_fields = ("field",)
    exclude = ("created_by", "updated_by")


@admin.register(NumberFieldConfig)
class NumberFieldConfigAdmin(ModelAdmin):
    list_display = ("field", "created_at", "updated_at")
    search_fields = ("field",)
    exclude = ("created_by", "updated_by")


@admin.register(BooleanFieldConfig)
class BooleanFieldConfigAdmin(ModelAdmin):
    list_display = ("field", "created_at", "updated_at")
    search_fields = ("field",)
    exclude = ("created_by", "updated_by")


@admin.register(DateFieldConfig)
class DateFieldConfigAdmin(ModelAdmin):
    list_display = ("field", "created_at", "updated_at")
    search_fields = ("field",)
    exclude = ("created_by", "updated_by")


@admin.register(ChecklistFieldConfig)
class ChecklistFieldConfigAdmin(ModelAdmin):
    list_display = ("field", "created_at", "updated_at")
    search_fields = ("field",)
    exclude = ("created_by", "updated_by")


@admin.register(ChoiceFieldConfig)
class ChoiceFieldConfigAdmin(ModelAdmin):
    list_display = ("field", "created_at", "updated_at")
    search_fields = ("field",)
    exclude = ("created_by", "updated_by")


class ViewInline(StackedInline):
    model = View
    extra = 0
    exclude = ("created_by", "updated_by")


# class FieldInline(StackedInline):
#     model = Field
#     extra = 0
#     exclude = ("created_by", "updated_by")
#     fields = ("label", "field_type")


@admin.register(Database)
class DatabaseAdmin(ModelAdmin):
    list_display = ("name", "workspace", "created_at", "updated_at")
    search_fields = ("name",)
    list_filter = ("workspace",)
    exclude = ("created_by", "updated_by")

    inlines = [FieldInline, ViewInline]


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


@admin.register(Page)
class PageAdmin(ModelAdmin):
    list_display = ("title", "database", "created_at", "updated_at")
    search_fields = ("title",)
    list_filter = ("database",)
    exclude = ("created_by", "updated_by")


@admin.register(Attachment)
class AttachmentAdmin(ModelAdmin):
    list_display = ("file", "created_at", "updated_at")
    exclude = ("created_by", "updated_by")
