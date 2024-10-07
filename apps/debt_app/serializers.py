from .models import DebtModel
from rest_framework import serializers

from ..product_app.models import DocumentModel


class DebtModelSerializer(serializers.ModelSerializer):
    amount = serializers.SerializerMethodField()

    class Meta:
        model = DebtModel
        fields = (
            'id', 'name', 'phone_number',
            'phone_number2', 'is_paid', 'amount'
        )

    def get_amount(self, debt: DebtModel):
        if debt.amount:
            return debt.amount
        else:
            docs = DocumentModel.objects.filter(
                debts__id=debt.id
            )

            total_amount = sum(
                item.discount_price if item.discount_price else item.selling_price
                for doc in docs
                for item in doc.items.all()
            )

            return total_amount
