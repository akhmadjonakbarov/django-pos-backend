from rest_framework import serializers
from .models import ProviderModel


class ProviderModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderModel
        fields = '__all__'
