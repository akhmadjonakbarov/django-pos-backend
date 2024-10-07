from rest_framework import serializers
from . import common_serializers
from . import document_serializers
from ..models import DocumentItemBalanceModel, ItemModel
from ...currency_app.serializers import CurrencyModelSerializer


class StoreItemModelSerializer(serializers.ModelSerializer):
    category = common_serializers.CategoryModelSerializer(read_only=True)
    company = common_serializers.CompanyModelSerializer(read_only=True)
    unit = common_serializers.UnitModelSerializer(read_only=True)

    class Meta:
        model = ItemModel
        fields = (
            'id', 'company', 'category', 'unit',
            'created_at', 'updated_at', 'name',
            'barcode',
        )


class StoreDocumentItemBalanceModelSerializer(serializers.ModelSerializer):
    item = StoreItemModelSerializer(read_only=True)
    document = document_serializers.DocumentModelSerializer(read_only=True)
    currency = CurrencyModelSerializer(read_only=True)

    class Meta:
        model = DocumentItemBalanceModel
        fields = (
            'id', 'item', 'can_be_cheaper', 'income_price_usd',
            'income_price', 'selling_price', 'discount_price',
            'selling_percentage', 'created_at', 'updated_at', 'qty',
            'document', 'currency'
        )
