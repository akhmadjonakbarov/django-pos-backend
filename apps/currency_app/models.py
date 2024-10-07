from django.db import models

from apps.base_app.models import BaseModel
from apps.user_app.models import CustomUserModel


class CurrencyModel(BaseModel):
    value = models.DecimalField(
        decimal_places=3, max_digits=15,
        default=0.0, null=True
    )  # Using FloatField for DOUBLE type
    deleted_at = models.DateTimeField(null=True, blank=True)  # Soft delete field
    user = models.ForeignKey(
        CustomUserModel,
        on_delete=models.CASCADE,  # Use SET_NULL if the user is deleted
        null=True,
        blank=True,
        related_name='currencies'
    )

    class Meta:
        db_table = 'currency'  # Specify the database table name
        verbose_name_plural = 'currencies'
        ordering = ['-id']  # Order by ID in descending order by default

    def __str__(self):
        return f'{self.value} UZS'
