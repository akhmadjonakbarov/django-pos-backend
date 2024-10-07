from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from ..models import DocumentItemBalanceModel
from ..serializers.store_serializers import StoreDocumentItemBalanceModelSerializer
from ...base_app.views import BaseDeleteView
from ...utils.response_messages import ResponseMessages
from ...utils.response_type import res_error, response_list, response_item

from django.db import transaction


class BaseView(GenericAPIView):
    queryset = DocumentItemBalanceModel
    permission_classes = None
    serializer_class = StoreDocumentItemBalanceModelSerializer


class GetRemainedItemListView(BaseView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, req):
        try:
            item_balances = self.queryset.objects.all().filter(is_deleted=False).order_by('-created_at')
            serializer = self.serializer_class(item_balances, many=True)
            return response_list(lst=serializer.data)
        except Exception as e:
            return res_error(str(e))


class UpdateItemBalanceView(BaseView):
    permission_classes = (IsAuthenticated,)

    def patch(self, req: Request, pk):
        try:
            qty = req.data.get('qty')
            selling_price = req.data.get('selling_price')
            selling_percentage = req.data.get('selling_percentage')

            item_balance: DocumentItemBalanceModel = self.queryset.objects.filter(pk=pk).first()
            item = item_balance.item
            with transaction.atomic():
                # Update both item_balance and item attributes
                item_balance.qty = qty
                item_balance.selling_price = selling_price
                item_balance.selling_percentage = selling_percentage
                item_balance.save()

                # If item fields are updated, do it here
                item.qty = qty
                item.selling_price = selling_price
                item.selling_percentage = selling_percentage
                item.save()
            return response_item(
                item=self.serializer_class(item_balance).data, message=ResponseMessages.SUCCESS,
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return res_error(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeleteItemBalanceView(BaseView, BaseDeleteView):
    permission_classes = (IsAuthenticated,)

    def delete(self, req, pk):
        try:
            return self.delete_instance(req, pk)
        except Exception as e:
            return res_error(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
