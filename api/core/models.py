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

    text_fields = models.ForeignKey("core.TextField", on_delete=models.CASCADE, blank=True, null=True)
    number_fields = models.ForeignKey("core.NumberField", on_delete=models.CASCADE, blank=True, null=True)
    boolean_fields = models.ForeignKey("core.BooleanField", on_delete=models.CASCADE, blank=True, null=True)
    date_fields = models.ForeignKey("core.DateField", on_delete=models.CASCADE, blank=True, null=True)
    checklist_fields = models.ForeignKey("core.ChecklistField", on_delete=models.CASCADE, blank=True, null=True)
    choice_fields = models.ForeignKey("core.ChoiceField", on_delete=models.CASCADE, blank=True, null=True)
    file_fields = models.ForeignKey("core.FileField", on_delete=models.CASCADE, blank=True, null=True)
    relation_fields = models.ForeignKey("core.RelationField", on_delete=models.CASCADE, blank=True, null=True)

    fields_order = ArrayField(models.UUIDField(), blank=True, default=list)
    sort_by = ArrayField(ArrayField(models.CharField(max_length=255), size=2), blank=True, default=list)
    filter_by = models.TextField(blank=True)

    def __str__(self):
        return self.label

    def clean(self):
        if self.is_default:
            View.objects.filter(database=self.database).exclude(pk=self.pk).update(is_default=False)

        if hasattr(self, "sort_by") and self.sort_by is not None and len(self.sort_by) > 0:
            for sort in self.sort_by:
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

    database = models.ForeignKey("core.Database", on_delete=models.CASCADE)
    label = models.CharField(max_length=255)
    field_type = models.IntegerField(choices=FieldType.choices)

    class Meta:
        abstract = True


class FieldResponse(BaseModel):
    page = models.ForeignKey("core.Page", on_delete=models.CASCADE)

    class Meta:
        abstract = True


class TextField(Field):
    class TextFormat(models.TextChoices):
        SINGLE_LINE = "single_line", "Single Line"
        MULTI_LINE = "multi_line", "Multi Line"
        EMAIL = "email", "Email"
        URL = "url", "URL"
        PHONE = "phone", "Phone"
        RICH_TEXT = "rich_text", "Rich Text"

    field_type = Field.FieldType.TEXT
    display_format = models.CharField(max_length=255, choices=TextFormat.choices, default=TextFormat.SINGLE_LINE)


class TextFieldResponse(FieldResponse):
    field = models.ForeignKey("core.TextField", on_delete=models.CASCADE)
    value = models.TextField(blank=True)

    def __str__(self):
        return self.value

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["page", "field"], name="unique_text_field_response"),
        ]


class NumberField(Field):
    class NumberFormat(models.TextChoices):
        DECIMAL = "decimal", "Decimal"
        INTEGER = "integer", "Integer"
        PERCENTAGE = "percentage", "Percentage"
        CURRENCY = "currency", "Currency"

    display_format = models.CharField(max_length=255, choices=NumberFormat.choices, default=NumberFormat.DECIMAL)


class NumberFieldResponse(FieldResponse):
    field = models.ForeignKey("core.NumberField", on_delete=models.CASCADE)
    value = models.FloatField()

    def __str__(self):
        return str(self.value)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["page", "field"], name="unique_number_field_response"),
        ]


class BooleanField(Field):
    class BooleanFormat(models.TextChoices):
        CHECKBOX = "checkbox", "Checkbox"
        TOGGLE = "toggle", "Toggle"

    display_format = models.CharField(max_length=255, choices=BooleanFormat.choices, default=BooleanFormat.CHECKBOX)


class BooleanFieldResponse(FieldResponse):
    field = models.ForeignKey("core.BooleanField", on_delete=models.CASCADE)
    value = models.BooleanField()

    def __str__(self):
        return str(self.value)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["page", "field"], name="unique_boolean_field_response"),
        ]


class DateField(Field):
    class DateFormat(models.TextChoices):
        DATE = "date", "Date"
        DATE_TIME = "datetime", "Date & Time"
        TIME = "time", "Time"

    display_format = models.CharField(max_length=255, choices=DateFormat.choices, default=DateFormat.DATE)


class DateFieldResponse(FieldResponse):
    field = models.ForeignKey("core.DateField", on_delete=models.CASCADE)
    value = models.DateTimeField()
    timezone = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return str(self.value)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["page", "field"], name="unique_date_field_response"),
        ]


class ChecklistField(Field):
    class ChecklistStatusFormat(models.TextChoices):
        PROGRESS_BAR = "progress", "Progress"
        PERCENTAGE = "percentage", "Percentage"

    status_format = models.CharField(
        max_length=255, choices=ChecklistStatusFormat.choices, default=ChecklistStatusFormat.PROGRESS_BAR
    )

    def clean(self):
        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class ChecklistFieldResponse(FieldResponse):
    field = models.ForeignKey("core.ChecklistField", on_delete=models.CASCADE)
    value = ArrayField(ArrayField(models.CharField(max_length=255), size=2))

    def __str__(self):
        return self.value

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["page", "field"], name="unique_checklist_field_response"),
        ]


class ChoiceField(Field):
    class ChoiceFormat(models.TextChoices):
        DROPDOWN = "dropdown", "Dropdown"
        RADIO = "radio", "Radio"
        CHECKBOX = "checkbox", "Checkbox"
        TAGS = "tags", "Tags"

    is_multi_select = models.BooleanField(default=False)
    display_format = models.CharField(max_length=255, choices=ChoiceFormat.choices, default=ChoiceFormat.DROPDOWN)

    def clean(self):
        if self.is_multi_select and self.display_format == ChoiceField.ChoiceFormat.RADIO:
            raise ValidationError("Cannot have radio display format when multi select is enabled")

        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class ChoiceFieldOption(BaseModel):
    field = models.ForeignKey("core.ChoiceField", on_delete=models.CASCADE, related_name="options")
    label = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    def __str__(self):
        return self.label


class ChoiceFieldResponse(FieldResponse):
    field = models.ForeignKey("core.ChoiceField", on_delete=models.CASCADE)
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


class FileField(Field):
    class FileTypes(models.TextChoices):
        ALL = "all", "All"
        IMAGE = "image"
        VIDEO = "video"
        AUDIO = "audio"
        DOCUMENT = "document"

    supported_file_types = ArrayField(models.CharField(max_length=255), blank=True)
    is_multiple = models.BooleanField(default=False)

    def clean(self):
        if len(self.supported_file_types) == 0:
            self.supported_file_types = [FileField.FileTypes.ALL]

        if FileField.FileTypes.ALL in self.supported_file_types and len(self.supported_file_types) > 1:
            raise ValidationError("Cannot have other file types when 'all' is selected")

        for file_type in self.supported_file_types:
            if file_type not in FileField.FileTypes.values:
                raise ValidationError(f"{file_type} is not a valid file type")

        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class FileFieldResponse(FieldResponse):
    field = models.ForeignKey("core.FileField", on_delete=models.CASCADE)
    attachments = models.ManyToManyField("core.Attachment", related_name="responses")

    def __str__(self):
        return self.file.name

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["page", "field"], name="unique_file_field_response"),
        ]


class RelationField(Field):
    database = models.ForeignKey("core.Database", on_delete=models.CASCADE)
    related_database = models.ForeignKey("core.Database", on_delete=models.CASCADE, related_name="related_field")

    def clean(self):
        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

        opposite_relation_field = RelationField.objects.filter(
            database=self.related_database, related_database=self.database
        )
        if not opposite_relation_field.exists():
            RelationField.objects.create(
                database=self.related_database,
                related_database=self.database,
                label=f"{self.label} (Related)",
            )


class RelationFieldResponse(FieldResponse):
    field = models.ForeignKey("core.RelationField", on_delete=models.CASCADE)
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
