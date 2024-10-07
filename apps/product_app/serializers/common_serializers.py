from rest_framework import serializers

from ..models import CategoryModel, CompanyModel, ItemModel, UnitModel, ColorModel, ItemColor, DocumentItemModel
from ...currency_app.serializers import CurrencyModelSerializer


class CompanyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyModel
        fields = ('id', 'name', 'created_at', 'updated_at')


class CategoryModelSerializer(serializers.ModelSerializer):
    items_type_count = serializers.SerializerMethodField(read_only=True)
    items_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CategoryModel
        fields = ('id', 'name', 'created_at', 'updated_at', 'items_type_count', 'items_count')

    def get_items_type_count(self, category: CategoryModel):
        return category.items.count()

    def get_items_count(self, category: CategoryModel):
        items_count = len([item for item in category.items.all() if item.doc_items.count() > 0]) or 0
        return items_count


class UnitModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitModel
        fields = ('id', 'value')


class ColorModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColorModel
        fields = '__all__'


class ItemColorSerializer(serializers.ModelSerializer):
    color = ColorModelSerializer()  # Make it writable

    class Meta:
        model = ItemColor
        fields = ('id', 'color', 'created_at', 'updated_at')


class DocumentItemModelSerializerForItem(serializers.ModelSerializer):
    currency = CurrencyModelSerializer()

    class Meta:
        model = DocumentItemModel
        fields = (
            'id', 'item', 'created_at', 'updated_at',
            'qty', 'selling_price', 'discount_price', 'selling_percentage',
            'income_price_usd', 'income_price', 'can_be_cheaper', 'document', 'currency'
        )


class ItemModelSerializer(serializers.ModelSerializer):
    company = CompanyModelSerializer()  # Make it writable
    category = CategoryModelSerializer()  # Make it writable
    unit = UnitModelSerializer()  # Make it writable
    doc_item = serializers.SerializerMethodField()

    class Meta:
        model = ItemModel
        fields = (
            'id', 'company', 'category', 'unit',
            'created_at', 'updated_at', 'name',
            'barcode', 'doc_item'
        )

    def get_doc_item(self, item: ItemModel):
        if item.doc_items.count() == 0:
            return None
        return DocumentItemModelSerializerForItem(item.doc_items.first(), many=False).data
