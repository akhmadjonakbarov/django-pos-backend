from rest_framework import serializers
from .models import BuilderModel


class BuilderModelSerializer(serializers.ModelSerializer):
    total_buying_price = serializers.SerializerMethodField()

    class Meta:
        model = BuilderModel
        fields = (
        'id', 'fish', 'phone_number', 'phone_number2', 'address', 'total_buying_price', 'created_at', 'updated_at')

    def get_total_buying_price(self, builder: BuilderModel):
        total_amount = 0
        documents = builder.documents.all()
        for document in documents:
            items = document.items.all()
            for item in items:
                if item.discount_price:
                    price = item.discount_price
                else:
                    price = item.selling_price
                total_amount = total_amount + (price * item.qty)
        return total_amount
