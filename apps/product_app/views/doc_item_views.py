from django.db import transaction
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from ..models import DocumentItemModel, DocumentModel, DocumentItemBalanceModel

from apps.utils.response_type import res_error, response_list, res_message
from ..serializers.document_item_balance_serializers import DocumentItemBalanceModelSerializer
from ...base_app.views import BaseListView
from ..serializers import doc_item_serializers
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

    def delete(self, request, pk):
        try:
            with transaction.atomic():
                doc_item: DocumentItemModel = self.queryset.active_objects().get(pk=pk)
                print(doc_item)
                try:
                    item_balance = DocumentItemBalanceModel.active_objects().get(
                        doc_item=doc_item
                    )

                    item_balance.qty += doc_item.qty
                    item_balance.save()
                except DocumentItemBalanceModel.DoesNotExist:
                    DocumentItemBalanceModel.objects.create(
                        item=doc_item.item,
                        doc_item=doc_item,
                        currency=doc_item.currency,
                        user=doc_item.user,
                        selling_price=doc_item.selling_price,
                        selling_percentage=doc_item.selling_percentage,
                        document_id=doc_item.document_id,
                        income_price=doc_item.income_price,
                        income_price_usd=doc_item.income_price_usd,
                        qty=doc_item.qty,
                        can_be_cheaper=doc_item.can_be_cheaper,
                        discount_price=doc_item.discount_price,
                    )

                document: DocumentModel = DocumentModel.active_objects().get(
                    id=doc_item.document_id
                )
                doc_items = document.items.all()
                if doc_items.count() > 1:
                    doc_item.delete()
                else:
                    doc_item.delete()
                    document.delete()
                return res_message(message=ResponseMessages.SUCCESS, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return res_error(str(e))
