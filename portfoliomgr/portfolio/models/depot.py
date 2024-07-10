from django.db import models

from .institute import Institute
from .person import Person
from .portfolio import Portfolio


class Depot(models.Model):
    name = models.CharField(max_length=100, blank=False, verbose_name="Name")
    fk_institute = models.ForeignKey(
        Institute,
        on_delete=models.CASCADE,
        verbose_name="Institute",
    )
    fk_portfolio = models.ForeignKey(
        Portfolio, on_delete=models.CASCADE, verbose_name="Portfolio"
    )
    fk_owner = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name="Owner")
    is_active = models.BooleanField(default=True, verbose_name="Active")

    def __str__(self):
        return f"{self.name} ({self.fk_owner.surname} - {self.fk_institute.short_name})"
