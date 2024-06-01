import json

from dateutil import parser
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.db import models

from api.models import BaseModel


class Database(BaseModel):
    workspace = models.ForeignKey("organizations.Workspace", on_delete=models.CASCADE, related_name="databases")

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

        has_views = View.objects.filter(database=self).exists()
        if not has_views:
            View.objects.create(
                database=self,
                label="Table",
                view_type=View.ViewType.TABLE,
                is_default=True,
            )

        has_page_view = View.objects.filter(database=self, view_type=View.ViewType.PAGE).exists()
        if not has_page_view:
            View.objects.create(
                database=self,
                label="Page",
                view_type=View.ViewType.PAGE,
            )


class View(BaseModel):
    class ViewType(models.IntegerChoices):
        TABLE = 0
        GRID = 10
        LIST = 20
        KANBAN = 30
        CALENDAR = 40
        PAGE = 100

    database = models.ForeignKey("core.Database", on_delete=models.CASCADE, related_name="views")

    label = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    view_type = models.IntegerField(choices=ViewType.choices, default=ViewType.TABLE)
    is_default = models.BooleanField(default=False)
    fields = models.ManyToManyField("core.Field", blank=True, related_name="views")
    fields_order = ArrayField(models.UUIDField(), blank=True, default=list)
    sort_by = ArrayField(ArrayField(models.CharField(max_length=255), size=2), blank=True, default=list)
    filter_by = models.TextField(blank=True)

    def __str__(self):
        return self.label

    def clean(self):
        if self.is_default:
            View.objects.filter(database=self.database).exclude(pk=self.pk).update(is_default=False)

        field_ids = set([field.id for field in self.fields.all()])
        field_order_ids = set([field_id for field_id in self.fields_order])
        non_overlap = field_ids.symmetric_difference(field_order_ids)
        if len(non_overlap) > 0:
            raise ValidationError("Fields and fields_order must be the same")

        if hasattr(self, "sort_by") and self.sort_by is not None and len(self.sort_by) > 0:
            for sort in self.sort_by:
                if len(sort) != 2:
                    raise ValidationError("Sort order must be a list of two items")

                if sort[0] not in field_ids:
                    raise ValidationError("Sort field must be in fields")

                if sort[1] not in ["asc", "desc"]:
                    raise ValidationError("Sort order must be 'asc' or 'desc'")

        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Folder(BaseModel):
    workspace = models.ForeignKey("organizations.Workspace", on_delete=models.CASCADE, related_name="folders")
    parent = models.ForeignKey(
        "core.Folder", on_delete=models.CASCADE, blank=True, null=True, related_name="child_folders"
    )
    label = models.CharField(max_length=255)
    views = models.ManyToManyField("core.View", blank=True, related_name="folders")
    view_order = ArrayField(models.UUIDField(), blank=True)

    def __str__(self):
        return self.label

    def clean(self):
        view_ids = set([view.id for view in self.views.all()])
        view_order_ids = set([view_id for view_id in self.view_order])
        non_overlap = view_ids.symmetric_difference(view_order_ids)
        if len(non_overlap) > 0:
            raise ValidationError("Views and view_order must be the same")

        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Page(BaseModel):
    database = models.ForeignKey("core.Database", on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    attachments = models.ManyToManyField("core.Attachment", blank=True, related_name="pages")

    def __str__(self):
        return self.title

    def clean(self):
        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Attachment(BaseModel):
    file = models.FileField(upload_to="attachments")

    def __str__(self):
        return self.file.name


class Field(BaseModel):
    class FieldType(models.TextChoices):
        BOOLEAN = "boolean", "Boolean"
        CHECKLIST = "checklist", "Checklist"
        CHOICE = "choice", "Choice"
        DATE = "date", "Date"
        FILE = "file", "File"
        NUMBER = "number", "Number"
        RELATION = "relation", "Relation"
        TEXT = "text", "Text"

    _config_field_map = {
        FieldType.BOOLEAN: "boolean_config",
        FieldType.CHECKLIST: "checklist_config",
        FieldType.CHOICE: "choice_config",
        FieldType.DATE: "date_config",
        FieldType.FILE: "file_config",
        FieldType.NUMBER: "number_config",
        FieldType.RELATION: "relation_config",
        FieldType.TEXT: "text_config",
    }

    database = models.ForeignKey("core.Database", on_delete=models.CASCADE)
    label = models.CharField(max_length=255)
    field_type = models.CharField(max_length=32, choices=FieldType.choices)

    boolean_config = models.OneToOneField("core.BooleanFieldConfig", on_delete=models.SET_NULL, blank=True, null=True)
    checklist_config = models.OneToOneField(
        "core.ChecklistFieldConfig", on_delete=models.SET_NULL, blank=True, null=True
    )
    choice_config = models.OneToOneField("core.ChoiceFieldConfig", on_delete=models.SET_NULL, blank=True, null=True)
    date_config = models.OneToOneField("core.DateFieldConfig", on_delete=models.SET_NULL, blank=True, null=True)
    file_config = models.OneToOneField("core.FileFieldConfig", on_delete=models.SET_NULL, blank=True, null=True)
    number_config = models.OneToOneField("core.NumberFieldConfig", on_delete=models.SET_NULL, blank=True, null=True)
    relation_config = models.OneToOneField(
        "core.RelationFieldConfig", on_delete=models.SET_NULL, blank=True, null=True
    )
    text_config = models.OneToOneField("core.TextFieldConfig", on_delete=models.SET_NULL, blank=True, null=True)

    @property
    def config_field_name(self):
        field_type_enum = Field.FieldType(self.field_type)
        return self._config_field_map[field_type_enum]

    @property
    def config(self):
        return getattr(self, self.config_field_name)

    @property
    def config_model(self):
        return self.config.__class__

    def create_default_config(self):
        config = self.config_model.create_default(field=self)
        setattr(self, self.config_field_name, config)

    def __str__(self):
        return self.label

    def clean(self):
        has_config = getattr(self, self.config_field_name) is not None
        if not has_config:
            raise ValidationError(f"{self.config_field_name} is required for field type {self.field_type}")

        super().clean()

    def save(self, *args, **kwargs):
        if self.config is None:
            self.create_default_config()

        self.full_clean()
        super().save(*args, **kwargs)

        if self.field_type == Field.FieldType.RELATION:
            self.create_opposite_relation()

    def create_opposite_relation(self):
        if self.field_type != Field.FieldType.RELATION:
            return

        has_opposite = self.config.target_field.source_relations.filter(target_field=self).exists()
        if has_opposite:
            return

        Field.objects.create(
            database=self.config.target_field.database,
            label=f"{self.label} (Reverse)",
            field_type=Field.FieldType.RELATION,
            relation_config=RelationFieldConfig.objects.create(
                source_field=self.config.target_field, target_field=self
            ),
        )


class BooleanFieldConfig(BaseModel):
    class DisplayFormat(models.TextChoices):
        CHECKBOX = "checkbox", "Checkbox"
        TOGGLE = "toggle", "Toggle"

    display_format = models.CharField(max_length=255, choices=DisplayFormat.choices, default=DisplayFormat.CHECKBOX)

    def create_default(self, field):
        return BooleanFieldConfig.objects.create()

    def validate_response_data(self, data):
        if not isinstance(data, bool):
            raise ValidationError("Value must be a boolean")

    def deserialize_response_data(self, data):
        if isinstance(data, str):
            return data.lower().strip() in ["true", "1", "yes"]

        return bool(data)

    def serialize_response_data(self, data):
        obj = self.deserialize_response_data(data)
        return json.dumps(obj)


class ChecklistFieldConfig(BaseModel):
    class DisplayFormat(models.TextChoices):
        CHECKBOX = "checkbox", "Checkbox"
        SWITCH = "switch", "Switch"

    class StatusFormat(models.TextChoices):
        PROGRESS_BAR = "progress", "Progress"
        PERCENTAGE = "percentage", "Percentage"

    display_format = models.CharField(max_length=255, choices=DisplayFormat.choices, default=DisplayFormat.CHECKBOX)
    status_format = models.CharField(max_length=255, choices=StatusFormat.choices, default=StatusFormat.PROGRESS_BAR)

    def create_default(self, field):
        return ChecklistFieldConfig.objects.create()

    def validate_response_data(self, data):
        if not isinstance(data, list):
            raise ValidationError("Value must be a list")

        for item in data:
            if not isinstance(item, dict):
                raise ValidationError("Value must be a list of dictionaries")

            if "value" not in item:
                raise ValidationError("Value must have a key 'value'")

            if "is_checked" not in item:
                raise ValidationError("Value must have a key 'is_checked'")

            if "is_checked" in item and not isinstance(item["is_checked"], bool):
                raise ValidationError("is_checked must be a boolean")

    def deserialize_response_data(self, data):
        if not isinstance(data, list):
            data = [data]

        for item in data:
            if not isinstance(item, dict):
                item = {"value": item, "is_checked": False}

            if "value" not in item:
                item["value"] = ""

            if "is_checked" not in item:
                item["is_checked"] = False

            if not isinstance(item["value"], str):
                item["value"] = str(item["value"])

            if not isinstance(item["is_checked"], bool):
                item["is_checked"] = bool(item["is_checked"])

        return data

    def serialize_response_data(self, data):
        obj = self.deserialize_response_data(data)
        return json.dumps(obj)

    def clean(self):
        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class ChoiceFieldConfig(BaseModel):
    class DisplayFormat(models.TextChoices):
        DROPDOWN = "dropdown", "Dropdown"
        RADIO = "radio", "Radio"
        CHECKBOX = "checkbox", "Checkbox"
        TAGS = "tags", "Tags"

    is_multi_select = models.BooleanField(default=False)
    display_format = models.CharField(max_length=255, choices=DisplayFormat.choices, default=DisplayFormat.DROPDOWN)

    def create_default(self, field):
        return ChoiceFieldConfig.objects.create()

    def validate_response_data(self, data):
        if not isinstance(data, list):
            raise ValidationError("Value must be a list")

        for item in data:
            if not isinstance(item, str):
                raise ValidationError("Value must be a list of strings")

            choice = ChoiceFieldOption.objects.filter(field_config=self, pk=item)
            if not choice.exists():
                raise ValidationError("Value must be a list of choice IDs")

            found_choice = choice.first()
            if found_choice and found_choice.field_config != self:
                raise ValidationError("Choice must belong to the field config")

        if not self.is_multi_select and len(data) > 1:
            raise ValidationError("Cannot have multiple values when multi select is disabled")

    def deserialize_response_data(self, data):
        if not isinstance(data, list):
            data = [data]

        for item in data:
            if not isinstance(item, str):
                item = str(item)

            item_model = ChoiceFieldOption.objects.filter(field_config=self, pk=item)
            if item_model.exists():
                item = item_model.first()
            else:
                item = None

        return data

    def serialize_response_data(self, data):
        obj = self.deserialize_response_data(data)

        for item in obj:
            if item is not None:
                item = item.pk

        return json.dumps(obj)

    def clean(self):
        if self.is_multi_select and self.display_format == ChoiceFieldConfig.DisplayFormat.RADIO:
            raise ValidationError("Cannot have radio display format when multi select is enabled")

        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class ChoiceFieldOption(BaseModel):
    field_config = models.ForeignKey("core.ChoiceFieldConfig", on_delete=models.CASCADE, related_name="options")
    label = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    def __str__(self):
        return self.label


class DateFieldConfig(BaseModel):
    class DisplayFormat(models.TextChoices):
        DATE = "date", "Date"
        DATE_TIME = "datetime", "Date & Time"
        TIME = "time", "Time"

    display_format = models.CharField(max_length=255, choices=DisplayFormat.choices, default=DisplayFormat.DATE)

    def create_default(self, field):
        return DateFieldConfig.objects.create()

    def validate_response_data(self, data):
        if not isinstance(data, str):
            raise ValidationError("Value must be a string")

    def deserialize_response_data(self, data):
        return parser.parse(data)

    def serialize_response_data(self, data):
        obj = self.deserialize_response_data(data)
        iso_date = obj.isoformat()
        return json.dumps(iso_date)


class FileFieldConfig(BaseModel):
    class FileType(models.TextChoices):
        ALL = "all", "All"
        IMAGE = "image"
        VIDEO = "video"
        AUDIO = "audio"
        DOCUMENT = "document"

    supported_file_types = ArrayField(models.CharField(max_length=255), blank=True)
    is_multiple = models.BooleanField(default=False)

    def create_default(self, field):
        return FileFieldConfig.objects.create()

    def valiate_response_data(self, data):
        if not isinstance(data, list):
            raise ValidationError("Value must be a list")

        for item in data:
            if not isinstance(item, str):
                raise ValidationError("Value must be a list of strings")

            attachment = Attachment.objects.filter(pk=item)
            if not attachment.exists():
                raise ValidationError("Value must be a list of attachment IDs")

    def deserialize_response_data(self, data):
        if not isinstance(data, list):
            data = [data]

        for item in data:
            if not isinstance(item, str):
                item = str(item)

            attachment = Attachment.objects.filter(pk=item)
            if attachment.exists():
                item = attachment.first()
            else:
                item = None

        return data

    def serialize_response_data(self, data):
        obj = self.deserialize_response_data(data)

        for item in obj:
            if item is not None:
                item = item.pk

        return json.dumps(obj)

    def clean(self):
        if len(self.supported_file_types) == 0:
            self.supported_file_types = [FileFieldConfig.FileType.ALL]

        if FileFieldConfig.FileType.ALL in self.supported_file_types and len(self.supported_file_types) > 1:
            raise ValidationError("Cannot have other file types when 'all' is selected")

        for file_type in self.supported_file_types:
            if file_type not in FileFieldConfig.FileType.values:
                raise ValidationError(f"{file_type} is not a valid file type")

        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class NumberFieldConfig(BaseModel):
    class DisplayFormat(models.TextChoices):
        DECIMAL = "decimal", "Decimal"
        INTEGER = "integer", "Integer"
        PERCENTAGE = "percentage", "Percentage"
        CURRENCY = "currency", "Currency"

    display_format = models.CharField(max_length=255, choices=DisplayFormat.choices, default=DisplayFormat.DECIMAL)

    def create_default(self, field):
        return NumberFieldConfig.objects.create()

    def validate_response_data(self, data):
        if not isinstance(data, (int, float)):
            raise ValidationError("Value must be a number")

    def deserialize_response_data(self, data):
        if self.display_format == NumberFieldConfig.DisplayFormat.INTEGER:
            return int(data)

        if self.display_format == NumberFieldConfig.DisplayFormat.PERCENTAGE and isinstance(data, str):
            return float(data.strip("%")) / 100

        if self.display_format == NumberFieldConfig.DisplayFormat.CURRENCY and isinstance(data, str):
            return float(data.strip("$").replace(",", ""))

        return float(data)

    def serialize_response_data(self, data):
        obj = self.deserialize_response_data(data)
        return json.dumps(obj)


class RelationFieldConfig(BaseModel):
    source_field = models.ForeignKey("core.Field", on_delete=models.CASCADE, related_name="source_relations")
    target_field = models.ForeignKey("core.Field", on_delete=models.CASCADE, related_name="target_relations")

    def create_default(self, field):
        return RelationFieldConfig.objects.create(
            source_field=field,
            target_field=field,
        )

    def validate_response_data(self, data):
        if not isinstance(data, list):
            raise ValidationError("Value must be a list")

        for item in data:
            if not isinstance(item, str):
                raise ValidationError("Value must be a list of strings")

            page = Page.objects.filter(pk=item)
            if not page.exists():
                raise ValidationError("Value must be a list of page IDs")

            found_page = page.first()
            if found_page and found_page.database != self.target_field.database:
                raise ValidationError("Page must belong to the target database")

    def deserialize_response_data(self, data):
        if not isinstance(data, list):
            data = [data]

        for item in data:
            if not isinstance(item, str):
                item = str(item)

            page = Page.objects.filter(pk=item)
            if page.exists():
                item = page.first()
            else:
                item = None

        return data

    def serialize_response_data(self, data):
        obj = self.deserialize_response_data(data)

        for item in obj:
            if item is not None:
                item = item.pk

        return json.dumps(obj)

    def clean(self):
        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class TextFieldConfig(BaseModel):
    class DisplayFormat(models.TextChoices):
        SINGLE_LINE = "single_line", "Single Line"
        MULTI_LINE = "multi_line", "Multi Line"
        EMAIL = "email", "Email"
        URL = "url", "URL"
        PHONE = "phone", "Phone"
        RICH_TEXT = "rich_text", "Rich Text"

    display_format = models.CharField(max_length=255, choices=DisplayFormat.choices, default=DisplayFormat.SINGLE_LINE)

    def create_default(self, field):
        return TextFieldConfig.objects.create()

    def validate_response_data(self, data):
        if not isinstance(data, str):
            raise ValidationError("Value must be a string")

    def deserialize_response_data(self, data):
        return str(data)

    def serialize_response_data(self, data):
        obj = self.deserialize_response_data(data)
        return json.dumps(obj)


class FieldResponse(BaseModel):
    page = models.ForeignKey("core.Page", on_delete=models.CASCADE)
    field = models.ForeignKey("core.Field", on_delete=models.CASCADE)
    data = models.JSONField(default=dict)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["page", "field"], name="unique_field_response"),
        ]

    def __str__(self):
        return f"{self.page} - {self.field}"

    def clean(self):
        has_value_key = "value" in self.data
        has_other_keys = len(self.data.keys()) > 1

        if not has_value_key or has_other_keys:
            raise ValidationError("Value must have a single key 'data'")

        super().clean()

    def save(self, *args, **kwargs):
        validate_fn = getattr(self.field.config, "validate_response_data", None)
        if validate_fn is not None:
            validate_fn(self.data)

        self.full_clean()
        super().save(*args, **kwargs)
