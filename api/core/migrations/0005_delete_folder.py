# Generated by Django 5.0.6 on 2024-06-30 05:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0004_booleanfieldconfig_display_icon_and_more"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Folder",
        ),
    ]
