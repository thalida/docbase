from typing import Any

from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from unfold.admin import ModelAdmin, StackedInline
from unfold.decorators import display

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


class BaseFieldConfigAdmin(ModelAdmin):
    list_display = ()
    exclude = ("created_by", "updated_by", "created_at", "updated_at")
    search_fields = ()
    readonly_fields = ("field",)

    @display(description="Field")
    def display_field_link(self, obj):
        return mark_safe(
            f"""
            <a
                href="{reverse("admin:core_field_change", args=[obj.field.id])}"
                class="flex items-center justify-between bg-white border px-2 py-2 max-w-48 rounded shadow-sm text-gray-400 hover:text-gray-700 focus:outline-none dark:bg-gray-900 dark:border-gray-700 dark:text-gray-500 dark:hover:text-gray-200"
            >
                <span>{obj.field.label}</span>
                <span class="material-symbols-outlined md-18">chevron_right</span>
            </a>
            """
        )

    def get_list_display(self, request):
        list_display = [field.name for field in self.model._meta.get_fields() if field.name not in self.exclude]
        list_display.insert(0, list_display.pop(list_display.index("id")))

        # replace field with "get_field_display" method
        if "field" in list_display:
            list_display[list_display.index("field")] = "display_field_link"
        return list_display


@admin.register(BooleanFieldConfig)
class BooleanFieldConfigAdmin(BaseFieldConfigAdmin):
    pass


@admin.register(ChecklistFieldConfig)
class ChecklistFieldConfigAdmin(BaseFieldConfigAdmin):
    pass


class ChoiceOptionInline(StackedInline):
    model = ChoiceFieldOption
    extra = 0
    exclude = ("created_by", "updated_by")


@admin.register(ChoiceFieldConfig)
class ChoiceFieldConfigAdmin(BaseFieldConfigAdmin):
    inlines = [
        ChoiceOptionInline,
    ]

    def options(self, obj):
        return ", ".join([option.label for option in obj.options.all()])


@admin.register(DateFieldConfig)
class DateFieldConfigAdmin(BaseFieldConfigAdmin):
    pass


@admin.register(FileFieldConfig)
class FileFieldConfigAdmin(BaseFieldConfigAdmin):
    pass


@admin.register(NumberFieldConfig)
class NumberFieldConfigAdmin(BaseFieldConfigAdmin):
    pass


@admin.register(RelationFieldConfig)
class RelationFieldConfigAdmin(BaseFieldConfigAdmin):
    pass


@admin.register(TextFieldConfig)
class TextFieldConfigAdmin(BaseFieldConfigAdmin):
    pass


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
    filter_horizontal = ("fields",)


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
