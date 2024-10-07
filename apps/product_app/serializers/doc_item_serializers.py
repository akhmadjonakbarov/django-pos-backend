from rest_framework import serializers
from . import common_serializers
from . import document_serializers
from apps.product_app import models as product_models
from ...currency_app.serializers import CurrencyModelSerializer


class DocumentItemModelSerializer(serializers.ModelSerializer):
    item = common_serializers.ItemModelSerializer()
    document = document_serializers.DocumentModelSerializer()
    currency = CurrencyModelSerializer(read_only=True)

    class Meta:
        model = product_models.DocumentItemModel
        fields = (
            'id', 'item', 'created_at', 'updated_at',
            'qty', 'selling_price', 'discount_price', 'selling_percentage',
            'income_price_usd', 'income_price', 'can_be_cheaper',
            'document', 'currency'
        )


class DocumentItemModelSerializerForItem(serializers.ModelSerializer):
    document = document_serializers.DocumentModelSerializer()

    class Meta:
        model = product_models.DocumentItemModel
        fields = (
            'id', 'created_at', 'updated_at',
            'qty', 'selling_price', 'discount_price', 'selling_percentage',
            'income_price_usd', 'income_price', 'can_be_cheaper', 'document'
        )
