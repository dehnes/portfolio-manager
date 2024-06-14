# Register your models here.
from django.contrib import admin

from .models import Depot, Institute, Person, Portfolio


class PersonAdmin(admin.ModelAdmin):
    pass


class InstituteAdmin(admin.ModelAdmin):
    pass


class PortfolioAdmin(admin.ModelAdmin):
    pass


class DepotAdmin(admin.ModelAdmin):
    pass


admin.site.register(Person, PersonAdmin)
admin.site.register(Portfolio, PortfolioAdmin)
admin.site.register(Depot, DepotAdmin)
admin.site.register(Institute, InstituteAdmin)
