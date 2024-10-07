from django.db import models

from apps.base_app.models import BaseModel
from apps.user_app.models import CustomUserModel


class ProviderModel(BaseModel):
    fish = models.CharField(max_length=255, null=False)

    phone_number = models.CharField(
        max_length=9,
        unique=True,
        null=False
    )

    phone_number2 = models.CharField(
        max_length=9,
        unique=True,
        null=True,
        blank=True
    )

    address = models.CharField(max_length=255, null=False, blank=True)

    user = models.ForeignKey(
        CustomUserModel,
        on_delete=models.CASCADE,
        related_name='providers'
    )

    class Meta:
        db_table = 'provider'
