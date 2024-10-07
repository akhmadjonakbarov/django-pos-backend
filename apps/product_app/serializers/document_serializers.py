from rest_framework import serializers
from apps.product_app import models as product_models


class DocumentModelSerializer(serializers.ModelSerializer):
    type_of_items = serializers.SerializerMethodField(read_only=True)
    total_items_qty = serializers.SerializerMethodField(read_only=True)
    total_price = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = product_models.DocumentModel
        fields = (
            'id', 'reg_date', 'doc_type',
            'created_at', 'updated_at',
            'type_of_items', 'total_items_qty', 'total_price'
        )

    def get_type_of_items(self, doc: product_models.DocumentModel):
        return doc.items.count()

    def get_total_items_qty(self, doc: product_models.DocumentModel):
        items = doc.items.all()
        return sum(item.qty for item in items)

    def get_total_price(self, doc: product_models.DocumentModel):
        doc_items = doc.items.all()
        if doc.doc_type == product_models.DocumentModel.SELL:
            return sum(item.selling_price * item.qty for item in doc_items)
        else:
            return sum(item.income_price * item.qty for item in doc_items)
