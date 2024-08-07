# Generated by Django 5.0.6 on 2024-07-03 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio", "0012_depot_is_active"),
    ]

    operations = [
        migrations.AlterField(
            model_name="depot",
            name="is_active",
            field=models.BooleanField(default=True, verbose_name="Active"),
        ),
        migrations.AlterField(
            model_name="institute",
            name="short_name",
            field=models.CharField(
                blank=True, default="", max_length=20, verbose_name="Short Name"
            ),
        ),
    ]
