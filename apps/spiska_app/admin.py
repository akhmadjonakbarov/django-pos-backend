from django.contrib import admin
from .models import SpiskaModel


# Register your models here.
@admin.register(SpiskaModel)
class SpiskaAdmin(admin.ModelAdmin):
    pass
