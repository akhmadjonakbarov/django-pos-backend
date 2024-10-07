from django.db import models

from apps.base_app import models as base_model
from apps.builder_app import models as builder_models
from apps.product_app import models as product_models
from apps.user_app import models as user_models


class DebtModel(base_model.BaseModel):
    id = models.AutoField(primary_key=True)  # Automatically creates an auto-incrementing primary key
    name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=15)  # Adjust max_length as needed
    phone_number2 = models.CharField(max_length=15, null=True, blank=True)  # Adjust max_length as needed
    address = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(
        user_models.CustomUserModel, on_delete=models.CASCADE,
        related_name='debts', blank=True, null=True
    )
    is_paid = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=15, decimal_places=3, default=0.0)
    document = models.ForeignKey(
        product_models.DocumentModel, on_delete=models.CASCADE, related_name='debts',
        null=True, blank=True,
    )
    builder = models.ForeignKey(
        builder_models.BuilderModel, on_delete=models.CASCADE,
        related_name='debts', null=True, blank=True
    )

    class Meta:
        db_table = 'debt'  # Adjust table name as needed
        verbose_name_plural = 'debts'
        ordering = ['id']  # Adjust ordering as needed

    def __str__(self):
        return self.name if self.name else f'Debt #{self.id}'
