from django.db import transaction
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from rest_framework.request import Request

from ..models import DocumentItemModel, DocumentModel, DocumentItemBalanceModel

from apps.utils.response_type import res_error, response_list, res_message
from ..serializers.document_item_balance_serializers import DocumentItemBalanceModelSerializer
from ...base_app.views import BaseListView
from ..serializers import doc_item_serializers
from ...spiska_app.models import SpiskaModel
from ...utils.response_messages import ResponseMessages


class BaseView(GenericAPIView):
    queryset = DocumentItemModel
    serializer_class = doc_item_serializers.DocumentItemModelSerializer


class ItemByDocumentIdListView(BaseView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, req, doc_id):
        try:
            items = self.queryset.active_objects().filter(document_id=doc_id)
            serializer = self.serializer_class(items, many=True)
            return response_list(
                lst=serializer.data,
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return res_error(str(e))


class ListView(BaseView, BaseListView):

    def get(self, req):
        try:
            return self.get_instances(req)
        except Exception as e:
            return res_error(str(e))


class BuyListView(BaseView):
    permission_classes = (AllowAny,)

    def get(self, req):
        try:
            items = DocumentItemBalanceModel.active_objects().filter(document__doc_type=DocumentModel.BUY)
            serializer = DocumentItemBalanceModelSerializer(items, many=True)
            return response_list(
                lst=serializer.data,
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return res_error(str(e))


class DeleteView(BaseView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request: Request, pk):
        try:
            with transaction.atomic():
                doc_item: DocumentItemModel = self.queryset.active_objects().get(
                    pk=pk,
                    document__doc_type=DocumentModel.SELL,
                )
                try:
                    item_balance: DocumentItemBalanceModel = DocumentItemBalanceModel.active_objects().get(
                        item=doc_item.item
                    )

                    item_balance.qty += doc_item.qty
                    item_balance.save()
                except DocumentItemBalanceModel.DoesNotExist:
                    DocumentItemBalanceModel.objects.create(
                        doc_item=doc_item,
                        item=doc_item.item,
                        qty=doc_item.qty,
                        income_price=doc_item.income_price,
                        selling_price=doc_item.selling_price,
                        user=request.user,
                        currency=doc_item.currency,
                        income_price_usd=doc_item.income_price_usd,
                        selling_percentage=doc_item.selling_percentage,
                        document=doc_item.document
                    )
                    spiska: SpiskaModel = SpiskaModel.active_objects().filter(item=doc_item.item).first()
                    if spiska:
                        spiska.hard_delete(spiska.pk)

                document_sell: DocumentModel = DocumentModel.active_objects().get(
                    id=doc_item.document_id, doc_type=DocumentModel.SELL
                )
                doc_items = document_sell.items.all().filter(is_deleted=False)
                if doc_items.count() > 1:
                    doc_item.delete()
                else:
                    doc_item.delete()
                    document_sell.delete()
                return res_message(message=ResponseMessages.SUCCESS, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return res_error(str(e))
