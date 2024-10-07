from rest_framework import serializers
from . import common_serializers
from . import document_serializers
from ..models import DocumentItemBalanceModel
from ...currency_app.serializers import CurrencyModelSerializer


class DocumentItemBalanceModelSerializer(serializers.ModelSerializer):
    item = common_serializers.ItemModelSerializer(read_only=True)
    document = document_serializers.DocumentModelSerializer(read_only=True)
    currency = CurrencyModelSerializer(read_only=True)

    class Meta:
        model = DocumentItemBalanceModel
        fields = (
            'id', 'item', 'created_at', 'updated_at',
            'qty', 'selling_price', 'discount_price', 'selling_percentage',
            'income_price_usd', 'income_price', 'can_be_cheaper',
            'document', 'currency'
        )
