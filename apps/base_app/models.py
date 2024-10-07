from django.db import models
from django.db.models import Manager, QuerySet
from django.utils import timezone


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True  # Ensure this model does not create a separate table
        ordering = ['-created_at']

    def delete(self, using=None, keep_parents=False):
        """Implement soft delete."""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        """Restore a soft-deleted object."""
        self.is_deleted = False
        self.deleted_at = None
        self.save()

    @classmethod
    def hard_delete(cls, pk):
        """Actually delete an object from the database."""
        cls.objects.filter(pk=pk).delete()

    @classmethod
    def all_objects(cls):
        """Retrieve all objects, including soft-deleted ones."""
        return cls.objects.all()  # Return all objects, including soft-deleted ones

    @classmethod
    def active_objects(cls) -> QuerySet:
        """Retrieve only non-deleted objects."""
        return cls.objects.filter(is_deleted=False)  # Filter out soft-deleted objects

    @classmethod
    def get_queryset(cls):
        """Get the default queryset for the model."""
        return cls.objects.filter(is_deleted=False)  # Use a default queryset that excludes soft-deleted records
