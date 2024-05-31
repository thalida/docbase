# from django.contrib import admin
# from unfold.admin import ModelAdmin, TabularInline, StackedInline

# from core.models import Attachment, BooleanField, ChecklistField, ChoiceField, Database, DateField, Field, Folder, NumberField, Page, TextField, View


# class ViewInline(StackedInline):
#     model = View
#     extra = 0
#     exclude = ("created_by", "updated_by")

# class FieldInline(StackedInline):
#     model = Field
#     extra = 0
#     exclude = ("created_by", "updated_by")

# @admin.register(Database)
# class DatabaseAdmin(ModelAdmin):
#     list_display = ("name", "workspace", "created_at", "updated_at")
#     search_fields = ("name",)
#     list_filter = ("workspace",)
#     exclude = ("created_by", "updated_by")

#     inlines = [FieldInline, ViewInline]


# @admin.register(View)
# class ViewAdmin(ModelAdmin):
#     list_display = ("label", "database", "created_at", "updated_at")
#     search_fields = ("label",)
#     list_filter = ("database",)
#     exclude = ("created_by", "updated_by")


# @admin.register(Folder)
# class FolderAdmin(ModelAdmin):
#     list_display = ("label", "workspace", "created_at", "updated_at")
#     search_fields = ("label",)
#     list_filter = ("workspace",)
#     exclude = ("created_by", "updated_by")


# @admin.register(Page)
# class PageAdmin(ModelAdmin):
#     list_display = ("title", "database", "created_at", "updated_at")
#     search_fields = ("title",)
#     list_filter = ("database",)
#     exclude = ("created_by", "updated_by")


# @admin.register(Attachment)
# class AttachmentAdmin(ModelAdmin):
#     list_display = ("file", "created_at", "updated_at")
#     exclude = ("created_by", "updated_by")


# @admin.register(Field)
# class FieldAdmin(ModelAdmin):
#     list_display = ("label", "database", "created_at", "updated_at")
#     search_fields = ("label",)
#     list_filter = ("database",)


# @admin.register(TextField)
# class TextFieldAdmin(ModelAdmin):
#     list_display = ("field", "created_at", "updated_at")
#     search_fields = ("field",)
#     exclude = ("created_by", "updated_by")


# @admin.register(NumberField)
# class NumberFieldAdmin(ModelAdmin):
#     list_display = ("field", "created_at", "updated_at")
#     search_fields = ("field",)
#     exclude = ("created_by", "updated_by")


# @admin.register(BooleanField)
# class BooleanFieldAdmin(ModelAdmin):
#     list_display = ("field", "created_at", "updated_at")
#     search_fields = ("field",)
#     exclude = ("created_by", "updated_by")


# @admin.register(DateField)
# class DateFieldAdmin(ModelAdmin):
#     list_display = ("field", "created_at", "updated_at")
#     search_fields = ("field",)
#     exclude = ("created_by", "updated_by")


# @admin.register(ChecklistField)
# class ChecklistFieldAdmin(ModelAdmin):
#     list_display = ("field", "created_at", "updated_at")
#     search_fields = ("field",)
#     exclude = ("created_by", "updated_by")


# @admin.register(ChoiceField)
# class ChoiceFieldAdmin(ModelAdmin):
#     list_display = ("field", "created_at", "updated_at")
#     search_fields = ("field",)
#     exclude = ("created_by", "updated_by")
