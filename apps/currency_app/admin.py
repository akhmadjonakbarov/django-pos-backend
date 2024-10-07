from django.contrib import admin
from .models import CurrencyModel


# Register your models here.
@admin.register(CurrencyModel)
class CurrencyModelAdmin(admin.ModelAdmin):
    pass
