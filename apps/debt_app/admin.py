from django.contrib import admin
from .models import DebtModel


# Register your models here.

@admin.register(DebtModel)
class DebtAdmin(admin.ModelAdmin):
    pass
