from django.db import models

from apps.base_app.models import BaseModel
from apps.user_app.models import CustomUserModel


class BuilderModel(BaseModel):
    id = models.AutoField(primary_key=True)  # Equivalent to autoIncrement in Sequelize

    fish = models.CharField(max_length=255)  # String field, can adjust max_length as needed

    phone_number = models.CharField(
        max_length=9,  # Ensure this matches the validation in Sequelize (len: [1, 9])
        unique=True,

    )

    phone_number2 = models.CharField(
        max_length=9,
        unique=True,
        null=True, blank=True
    )

    address = models.CharField(max_length=255)  # String field for address

    user = models.ForeignKey(
        CustomUserModel,
        on_delete=models.CASCADE  # This is the equivalent of `references` in Sequelize
    )

    # Soft delete functionality
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        # Model metadata
        db_table = 'builder'
        ordering = ['id']
        verbose_name_plural = 'builders'

    def __str__(self):
        return f"{self.fish} - {self.phone_number}"
