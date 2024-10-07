from django.db import models

# Create your models here.
from apps.base_app.models import BaseModel
from apps.product_app.models import ItemModel


class SpiskaModel(BaseModel):
    item = models.OneToOneField(ItemModel, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.item)

    class Meta:
        db_table = 'spiska'
        ordering = ['-id']  # Adjust ordering as needed
        verbose_name_plural = 'spiskas'
