# Generated by Django 5.0.6 on 2024-07-15 15:24

import datetime
import django.core.validators
import django.db.models.deletion
import django_resized.forms
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio", "0021_batchposition_blocking_date"),
    ]

    operations = [
        migrations.CreateModel(
            name="PaymentProvider",
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
                ("name", models.CharField(max_length=100)),
                (
                    "logo",
                    django_resized.forms.ResizedImageField(
                        crop=None,
                        force_format="PNG",
                        keep_meta=True,
                        quality=-1,
                        scale=None,
                        size=[300, 300],
                        upload_to="logos",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Dividend",
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
                    "amount",
                    models.DecimalField(
                        decimal_places=2, max_digits=14, verbose_name="Amount"
                    ),
                ),
                (
                    "taxes",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        default=0.0,
                        max_digits=14,
                        verbose_name="Taxes",
                    ),
                ),
                (
                    "payment_date",
                    models.DateField(
                        default=datetime.date.today, verbose_name="Payment Date"
                    ),
                ),
                (
                    "fk_security",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="Security",
                        to="portfolio.security",
                        verbose_name="Security",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PaymentCard",
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
                    "name",
                    models.CharField(blank=True, max_length=100, verbose_name="Name"),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("Credit", "Credit"),
                            ("Debit", "Debit"),
                            ("EC", "Electronic Cash"),
                            ("Other", "Other"),
                        ],
                        max_length=20,
                        verbose_name="Type",
                    ),
                ),
                (
                    "card_number",
                    models.CharField(max_length=24, verbose_name="Card Number"),
                ),
                (
                    "valid_month",
                    models.IntegerField(
                        default=1,
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(12),
                        ],
                    ),
                ),
                (
                    "valid_year",
                    models.IntegerField(
                        default=2022,
                        validators=[django.core.validators.MinValueValidator(2022)],
                    ),
                ),
                ("cvc", models.CharField(blank=True, max_length=3, verbose_name="CVC")),
                (
                    "karten_folge_nummer",
                    models.IntegerField(
                        blank=True,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                ("status", models.BooleanField(default=True, verbose_name="Active")),
                (
                    "fk_account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="portfolio.bankaccount",
                        verbose_name="Bank Account",
                    ),
                ),
                (
                    "fk_owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="portfolio.person",
                        verbose_name="Owner",
                    ),
                ),
                (
                    "fk_payment_service",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="portfolio.paymentprovider",
                        verbose_name="Payment Service",
                    ),
                ),
            ],
        ),
    ]
