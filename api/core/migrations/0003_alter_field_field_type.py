# Generated by Django 5.0.3 on 2024-06-01 03:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_remove_view_is_default_alter_view_view_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="field",
            name="field_type",
            field=models.CharField(
                choices=[
                    ("boolean", "Boolean"),
                    ("checklist", "Checklist"),
                    ("choice", "Choice"),
                    ("date", "Date"),
                    ("file", "File"),
                    ("number", "Number"),
                    ("relation", "Relation"),
                    ("text", "Text"),
                ],
                default="text",
                max_length=32,
            ),
        ),
    ]