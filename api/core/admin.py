from django.contrib import admin
from unfold.admin import ModelAdmin, StackedInline

from core.models import (
    Attachment,
    BooleanField,
    ChecklistField,
    ChoiceField,
    Database,
    DateField,
    FileField,
    Folder,
    NumberField,
    Page,
    RelationField,
    TextField,
    View,
)


class BaseFieldInline(StackedInline):
    extra = 0
    exclude = ("created_by", "updated_by")


class TextFieldInline(BaseFieldInline):
    model = TextField


class NumberFieldInline(BaseFieldInline):
    model = NumberField


class BooleanFieldInline(BaseFieldInline):
    model = BooleanField


class DateFieldInline(BaseFieldInline):
    model = DateField


class ChecklistFieldInline(BaseFieldInline):
    model = ChecklistField


class ChoiceFieldInline(BaseFieldInline):
    model = ChoiceField


class FileFieldInline(BaseFieldInline):
    model = FileField


class RelationFieldInline(BaseFieldInline):
    model = RelationField
    fk_name = "database"


@admin.register(TextField)
class TextFieldAdmin(ModelAdmin):
    list_display = ("created_at", "updated_at")
    search_fields = ()
    exclude = ("created_by", "updated_by")


@admin.register(NumberField)
class NumberFieldAdmin(ModelAdmin):
    list_display = ("created_at", "updated_at")
    search_fields = ()
    exclude = ("created_by", "updated_by")


@admin.register(BooleanField)
class BooleanFieldAdmin(ModelAdmin):
    list_display = ("created_at", "updated_at")
    search_fields = ()
    exclude = ("created_by", "updated_by")


@admin.register(DateField)
class DateFieldAdmin(ModelAdmin):
    list_display = ("created_at", "updated_at")
    search_fields = ()
    exclude = ("created_by", "updated_by")


@admin.register(ChecklistField)
class ChecklistFieldAdmin(ModelAdmin):
    list_display = ("created_at", "updated_at")
    search_fields = ()
    exclude = ("created_by", "updated_by")


@admin.register(ChoiceField)
class ChoiceFieldAdmin(ModelAdmin):
    list_display = ("created_at", "updated_at")
    search_fields = ()
    exclude = ("created_by", "updated_by")


@admin.register(FileField)
class FileFieldAdmin(ModelAdmin):
    list_display = ("created_at", "updated_at")
    search_fields = ()
    exclude = ("created_by", "updated_by")


@admin.register(RelationField)
class RelationFieldAdmin(ModelAdmin):
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
        ViewInline,
        TextFieldInline,
        NumberFieldInline,
        BooleanFieldInline,
        DateFieldInline,
        ChecklistFieldInline,
        ChoiceFieldInline,
        FileFieldInline,
        RelationFieldInline,
    ]


@admin.register(View)
class ViewAdmin(ModelAdmin):
    list_display = ("label", "database", "created_at", "updated_at")
    search_fields = ("label",)
    list_filter = ("database",)
    exclude = ("created_by", "updated_by")

    # inlines = [
    #     TextFieldInline,
    #     NumberFieldInline,
    #     BooleanFieldInline,
    #     DateFieldInline,
    #     ChecklistFieldInline,
    #     ChoiceFieldInline,
    #     FileFieldInline,
    #     RelationFieldInline,
    # ]


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
