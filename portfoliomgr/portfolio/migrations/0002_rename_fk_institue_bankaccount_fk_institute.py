# Generated by Django 5.0.6 on 2024-06-17 17:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="bankaccount",
            old_name="fk_institue",
            new_name="fk_institute",
        ),
    ]
