from rest_framework import serializers

from apps.product_app.serializers.common_serializers import ItemModelSerializer
from apps.spiska_app.models import SpiskaModel


class SpiskaModelSerializer(serializers.ModelSerializer):
    item = ItemModelSerializer(read_only=False, many=False)

    class Meta:
        model = SpiskaModel
        fields = '__all__'
