from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.product_app.models import DocumentItemModel, DocumentItemBalanceModel

from apps.base_app.views import BaseListView, BaseUpdateView, BaseDeleteView, GenericAPIView
from .db_helper import update_prices_and_bulk_update
from .models import CurrencyModel
from .serializers import CurrencyModelSerializer

from ..utils.response_type import response_item, res_error


class BaseView(GenericAPIView):
    queryset = CurrencyModel
    serializer_class = CurrencyModelSerializer


class ListView(BaseView, BaseListView):
    def get(self, request):
        return self.get_instances(request)


class AddView(BaseView):

    def post(self, request):
        user = request.user
        data = request.data

        try:
            new_currency = CurrencyModel.objects.create(
                user=user,
                value=data['value'],
            )

            # Update DocumentItemBalanceModel items
            item_balances = DocumentItemBalanceModel.active_objects()
            update_prices_and_bulk_update(item_balances, DocumentItemBalanceModel, new_currency)

            # Update DocumentItemModel items
            document_items = DocumentItemModel.active_objects().filter(document__doc_type='buy')
            update_prices_and_bulk_update(document_items, DocumentItemModel, new_currency)

            serializer = CurrencyModelSerializer(new_currency, many=False)

            return response_item(item=serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return res_error(error=e)


class UpdateView(BaseView, BaseUpdateView):

    def patch(self, request, pk):
        try:
            return self.update_instance(request, pk)
        except Exception as e:
            print(e)
            return res_error(error=e)


class DeleteView(BaseView, BaseDeleteView):
    def delete(self, request, pk):
        return self.delete_instance(request, pk)
