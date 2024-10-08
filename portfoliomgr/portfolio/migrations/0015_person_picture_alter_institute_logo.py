# Generated by Django 5.0.6 on 2024-07-03 14:20

import django_resized.forms
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio", "0014_institute_logo"),
    ]

    operations = [
        migrations.AddField(
            model_name="person",
            name="picture",
            field=django_resized.forms.ResizedImageField(
                crop=None,
                default=1,
                force_format="PNG",
                keep_meta=True,
                quality=-1,
                scale=None,
                size=[500, 500],
                upload_to="profile_pics",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="institute",
            name="logo",
            field=django_resized.forms.ResizedImageField(
                crop=None,
                force_format="PNG",
                keep_meta=True,
                quality=-1,
                scale=None,
                size=[300, 300],
                upload_to="logos",
            ),
        ),
    ]
