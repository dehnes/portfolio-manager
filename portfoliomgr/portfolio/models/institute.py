from django.db import models
from django_resized import ResizedImageField


class Institute(models.Model):
    bic = models.CharField(max_length=12, blank=False, unique=True, verbose_name="BIC")
    name = models.CharField(max_length=100, blank=False, verbose_name="Name")
    short_name = models.CharField(
        max_length=20, default="", blank=True, verbose_name="Short Name"
    )
    logo = ResizedImageField(size=[300, 300], upload_to="logos", force_format="PNG")

    def __str__(self):
        return self.name
