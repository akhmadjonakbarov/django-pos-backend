import json
import time

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from apps.currency_app.models import CurrencyModel
from apps.product_app.models import DocumentItemBalanceModel, DocumentModel, DocumentItemModel
from apps.utils.response_type import *
from .models import StatisticsModel
from .serializers import StatisticsSerializer


class StatisticsView(APIView):
    permission_classes = [AllowAny]

    def last_currency(self) -> CurrencyModel:

        return CurrencyModel.objects.last()

    def get(self, request):
        self.get_data()
        try:
            statistics = StatisticsModel.objects.all()
            serializer = StatisticsSerializer(statistics, many=True)
            return response_list(
                message=ResponseMessages.SUCCESS,
                lst=serializer.data,
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return res_error(error=e)

    def get_data(self):

        total_value_of_products_usd = 0
        total_value_of_products_uzs = 0
        currency_value = 0.0

        try:
            last_currency = self.last_currency()
            if last_currency is not None:
                currency_value = last_currency.value

            # Get active builders and add to statistics

            item_balances = DocumentItemBalanceModel.active_objects()
            for balance in item_balances:
                item_balance: DocumentItemBalanceModel = balance
                total_value_of_products_usd += item_balance.income_price_usd * balance.qty
                total_value_of_products_uzs += item_balance.income_price * balance.qty

            StatisticsModel.objects.update_or_create(
                name="total_value_of_products_usd", defaults={'value': total_value_of_products_usd}
            )

            total_uzs = (total_value_of_products_usd * currency_value) + total_value_of_products_uzs
            StatisticsModel.objects.update_or_create(
                name="total_value_of_products_uzs",

                defaults={
                    'value': total_uzs,
                }
            )

            # Calculate profit and add to statistics
            total_profit = 0

            sold_items = DocumentItemModel.objects.filter(
                document__doc_type=DocumentModel.SELL,
            )

            # Loop through each sold item and calculate the profit
            for item in sold_items:
                income_price_total = item.qty * item.income_price  # Total income price for the item

                # Check if there's a discount, and use the appropriate selling price
                if item.discount_price > 0:
                    selling_price_total = item.qty * item.discount_price  # Total discounted selling price
                else:
                    selling_price_total = item.qty * item.selling_price  # Total regular selling price

                # Calculate the profit for this item
                profit = selling_price_total - income_price_total

                # Accumulate the total profit for the month
                total_profit += profit
            StatisticsModel.objects.update_or_create(
                name="profit_for_month",
                defaults={
                    'value': total_profit,
                }
            )

        except Exception as e:
            raise e
