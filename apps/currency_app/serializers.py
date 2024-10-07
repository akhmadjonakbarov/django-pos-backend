from rest_framework import serializers
from .models import CurrencyModel


class CurrencyModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = CurrencyModel
        fields = ('id', 'value', 'created_at')
