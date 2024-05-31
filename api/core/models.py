from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.postgres.fields import ArrayField

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

        has_fields = self.fields.exists()
        has_fields_order = self.fields_order is not None and len(self.fields_order) > 0
        if has_fields and has_fields_order:
            field_ids = set([field.id for field in self.fields.all()])
            fields_order_ids = set([field_id for field_id in self.fields_order])
            non_overlap = field_ids.symmetric_difference(fields_order_ids)
            if len(non_overlap) > 0:
                raise ValidationError("Fields and fields_order must be the same")

        if hasattr(self, "sort_by") and self.sort_by is not None and len(self.sort_by) > 0:
            for sort in self.sort_by:
                if sort[0] not in self.fields:
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
    class FieldType(models.IntegerChoices):
        TEXT = 0
        NUMBER = 10
        DATE = 20
        BOOLEAN = 30
        CHOICE = 40
        CHECKLIST = 50
        FILE = 60
        RELATION = 100

    database = models.ForeignKey("core.Database", on_delete=models.CASCADE, related_name="fields")
    label = models.CharField(max_length=255)
    field_type = models.IntegerField(choices=FieldType.choices)

    def __str__(self):
        return self.label

    @property
    def config(self):
        if self.field_type == Field.FieldType.TEXT:
            return self.text_field_config

        elif self.field_type == Field.FieldType.NUMBER:
            return self.number_field_config

        elif self.field_type == Field.FieldType.BOOLEAN:
            return self.boolean_field_config

        elif self.field_type == Field.FieldType.DATE:
            return self.date_field_config

        elif self.field_type == Field.FieldType.CHECKLIST:
            return self.checklist_field_config

        elif self.field_type == Field.FieldType.CHOICE:
            return self.choice_field_config

        elif self.field_type == Field.FieldType.FILE:
            return self.file_field_config

        elif self.field_type == Field.FieldType.RELATION:
            return self.relation_field_config


class FieldResponse(BaseModel):
    page = models.ForeignKey("core.Page", on_delete=models.CASCADE)
    field = models.ForeignKey("core.Field", on_delete=models.CASCADE)

    class Meta:
        abstract = True


class TextFieldConfig(BaseModel):
    class TextFormat(models.TextChoices):
        SINGLE_LINE = "single_line", "Single Line"
        MULTI_LINE = "multi_line", "Multi Line"
        EMAIL = "email", "Email"
        URL = "url", "URL"
        PHONE = "phone", "Phone"
        RICH_TEXT = "rich_text", "Rich Text"

    field = models.OneToOneField("core.Field", on_delete=models.CASCADE, related_name="text_field_config")
    display_format = models.CharField(max_length=255, choices=TextFormat.choices, default=TextFormat.SINGLE_LINE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["field"], name="unique_text_field"),
        ]


class TextFieldResponse(FieldResponse):
    value = models.TextField(blank=True)

    def __str__(self):
        return self.value

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["page", "field"], name="unique_text_field_response"),
        ]


class NumberFieldConfig(BaseModel):
    class NumberFormat(models.TextChoices):
        DECIMAL = "decimal", "Decimal"
        INTEGER = "integer", "Integer"
        PERCENTAGE = "percentage", "Percentage"
        CURRENCY = "currency", "Currency"

    field = models.OneToOneField("core.Field", on_delete=models.CASCADE, related_name="number_field_config")
    display_format = models.CharField(max_length=255, choices=NumberFormat.choices, default=NumberFormat.DECIMAL)


class NumberFieldResponse(FieldResponse):
    value = models.FloatField()

    def __str__(self):
        return str(self.value)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["page", "field"], name="unique_number_field_response"),
        ]


class BooleanFieldConfig(BaseModel):
    class BooleanFormat(models.TextChoices):
        CHECKBOX = "checkbox", "Checkbox"
        TOGGLE = "toggle", "Toggle"

    field = models.OneToOneField("core.Field", on_delete=models.CASCADE, related_name="boolean_field_config")
    display_format = models.CharField(max_length=255, choices=BooleanFormat.choices, default=BooleanFormat.CHECKBOX)


class BooleanFieldResponse(FieldResponse):
    value = models.BooleanField()

    def __str__(self):
        return str(self.value)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["page", "field"], name="unique_boolean_field_response"),
        ]


class DateFieldConfig(BaseModel):
    class DateFormat(models.TextChoices):
        DATE = "date", "Date"
        DATE_TIME = "datetime", "Date & Time"
        TIME = "time", "Time"

    field = models.OneToOneField("core.Field", on_delete=models.CASCADE, related_name="date_field_config")
    display_format = models.CharField(max_length=255, choices=DateFormat.choices, default=DateFormat.DATE)


class DateFieldResponse(FieldResponse):
    value = models.DateTimeField()
    timezone = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return str(self.value)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["page", "field"], name="unique_date_field_response"),
        ]


class ChecklistFieldConfig(BaseModel):
    class ChecklistStatusFormat(models.TextChoices):
        PROGRESS_BAR = "progress", "Progress"
        PERCENTAGE = "percentage", "Percentage"

    field = models.OneToOneField("core.Field", on_delete=models.CASCADE, related_name="checklist_field_config")
    status_format = models.CharField(
        max_length=255, choices=ChecklistStatusFormat.choices, default=ChecklistStatusFormat.PROGRESS_BAR
    )

    def clean(self):
        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class ChecklistFieldResponse(FieldResponse):
    value = ArrayField(ArrayField(models.CharField(max_length=255), size=2))

    def __str__(self):
        return self.value

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["page", "field"], name="unique_checklist_field_response"),
        ]


class ChoiceFieldConfig(BaseModel):
    class ChoiceFormat(models.TextChoices):
        DROPDOWN = "dropdown", "Dropdown"
        RADIO = "radio", "Radio"
        CHECKBOX = "checkbox", "Checkbox"
        TAGS = "tags", "Tags"

    field = models.OneToOneField("core.Field", on_delete=models.CASCADE, related_name="choice_field_config")
    is_multi_select = models.BooleanField(default=False)
    display_format = models.CharField(max_length=255, choices=ChoiceFormat.choices, default=ChoiceFormat.DROPDOWN)

    def clean(self):
        if self.is_multi_select and self.display_format == ChoiceFieldConfig.ChoiceFormat.RADIO:
            raise ValidationError("Cannot have radio display format when multi select is enabled")

        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class ChoiceFieldOption(BaseModel):
    field = models.ForeignKey("core.ChoiceFieldConfig", on_delete=models.CASCADE, related_name="options")
    label = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    def __str__(self):
        return self.label


class ChoiceFieldResponse(FieldResponse):
    values = models.ManyToManyField("core.ChoiceFieldOption", related_name="responses")

    def __str__(self):
        return self.value

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["page", "field"], name="unique_choice_field_response"),
        ]

    def clean(self):
        if self.field.is_multi_select and self.values.count() > 1:
            raise ValidationError("Cannot have multiple values when multi select is enabled")

        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class FileFieldConfig(BaseModel):
    class FileTypes(models.TextChoices):
        ALL = "all", "All"
        IMAGE = "image"
        VIDEO = "video"
        AUDIO = "audio"
        DOCUMENT = "document"

    field = models.OneToOneField("core.Field", on_delete=models.CASCADE, related_name="file_field_config")
    supported_file_types = ArrayField(models.CharField(max_length=255), blank=True)
    is_multiple = models.BooleanField(default=False)

    def clean(self):
        if len(self.supported_file_types) == 0:
            self.supported_file_types = [FileFieldConfig.FileTypes.ALL]

        if FileFieldConfig.FileTypes.ALL in self.supported_file_types and len(self.supported_file_types) > 1:
            raise ValidationError("Cannot have other file types when 'all' is selected")

        for file_type in self.supported_file_types:
            if file_type not in FileFieldConfig.FileTypes.values:
                raise ValidationError(f"{file_type} is not a valid file type")

        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class FileFieldResponse(FieldResponse):
    attachments = models.ManyToManyField("core.Attachment", related_name="responses")

    def __str__(self):
        return self.file.name

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["page", "field"], name="unique_file_field_response"),
        ]


class RelationFieldConfig(BaseModel):
    field = models.OneToOneField("core.Field", on_delete=models.CASCADE, related_name="relation_field_config")
    database = models.ForeignKey("core.Database", on_delete=models.CASCADE)
    related_database = models.ForeignKey(
        "core.Database", on_delete=models.CASCADE, related_name="related_field_configs"
    )

    def clean(self):
        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

        opposite_relation_field = RelationFieldConfig.objects.filter(
            database=self.related_database, related_database=self.database
        )
        if not opposite_relation_field.exists():
            field = Field.objects.create(
                database=self.related_database,
                label=f"{self.related_database.name} (Related)",
                field_type=Field.FieldType.RELATION,
            )
            RelationFieldConfig.objects.create(
                field=field,
                database=self.related_database,
                related_database=self.database,
            )


class RelationFieldResponse(FieldResponse):
    related_pages = models.ManyToManyField("core.Page", related_name="related_fields")

    def __str__(self):
        return self.related_page.title

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["page", "field"], name="unique_relation_field_response"),
        ]

    def clean(self):
        if self.field.related_database != self.related_page.database:
            raise ValidationError("Related page must be in the related database")

        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
