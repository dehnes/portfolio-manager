# Generated by Django 5.0.6 on 2024-06-28 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio", "0010_alter_accountbooking_booking_date_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="accountbooking",
            name="description",
            field=models.TextField(
                blank=True, max_length=500, verbose_name="Description"
            ),
        ),
    ]