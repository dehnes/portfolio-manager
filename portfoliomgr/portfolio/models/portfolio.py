from django.db import models

from .person import Person


class Portfolio(models.Model):
    name = models.CharField(max_length=100, blank=False, verbose_name="Name")
    fk_owner = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name="Owner")

    def __str__(self):
        return self.name
