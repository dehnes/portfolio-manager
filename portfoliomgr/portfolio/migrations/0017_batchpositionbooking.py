# Generated by Django 5.0.6 on 2024-07-08 12:58

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio", "0016_alter_asset_unique_together"),
    ]

    operations = [
        migrations.CreateModel(
            name="BatchPositionBooking",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "quantity",
                    models.DecimalField(
                        decimal_places=2, max_digits=14, verbose_name="Quantity"
                    ),
                ),
                (
                    "booking_date",
                    models.DateField(
                        default=datetime.date.today, verbose_name="Booking Date"
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, max_length=500, verbose_name="Description"
                    ),
                ),
                (
                    "fk_batch_position",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="portfolio.batchposition",
                        verbose_name="Batch Position",
                    ),
                ),
                (
                    "fk_transaction",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="portfolio.transaction",
                        verbose_name="Transaction",
                    ),
                ),
            ],
        ),
    ]