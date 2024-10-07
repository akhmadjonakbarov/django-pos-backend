from django.contrib import admin
from .models import BuilderModel


# Register your models here.
@admin.register(BuilderModel)
class BuilderAdmin(admin.ModelAdmin):
    list_display = ('id', 'fish', 'address', 'phone_number')
