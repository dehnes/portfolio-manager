from django.db import models
from django_resized import ResizedImageField


class Person(models.Model):
    name = models.CharField(max_length=100, blank=False, verbose_name="Name")
    surname = models.CharField(max_length=100, blank=False, verbose_name="Surname")
    picture = ResizedImageField(
        size=[500, 500], upload_to="profile_pics", force_format="PNG"
    )

    def __str__(self):
        return f"{self.surname} {self.name}"
