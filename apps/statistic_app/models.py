from django.db import models

from apps.base_app.models import BaseModel


# Create your models here.
class StatisticsModel(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    value = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return f"{self.name} {self.value}"

    class Meta:
        db_table = 'statistic'
        verbose_name_plural = 'statistics'
        ordering = ['-id']
