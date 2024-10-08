import json
import math

from rest_framework import status
from rest_framework.generics import GenericAPIView
from django.db import transaction
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from apps.product_app.views.db_writers.create_document import create_document
from apps.utils.response_type import res_error, res_message, response_list
from apps.product_app.views.db_writers.manage_item import (
    create_doc_item, create_doc_item_balance,
    update_doc_item_balance
)
from .db_writers.create_debt import create_debt_for_builder, create_debt
from ..models import DocumentItemBalanceModel, DocumentModel, DocumentItemModel
from ..serializers.document_serializers import DocumentModelSerializer
from ...base_app.views import BaseListView, BaseDeleteView
from ...builder_app.models import BuilderModel
from ...spiska_app.models import SpiskaModel
from ...utils.response_messages import ResponseMessages
from django.utils.timezone import now, timedelta
from rest_framework.permissions import IsAuthenticated


class CreateBuyDocument(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request: Request):
        data = request.data
        try:
            doc_type = data.get('doc_type')
            product_doc_items = data.get('product_doc_items')
            with transaction.atomic():
                document = create_document(
                    doc_type=doc_type,
                    user=request.user
                )
                for index in range(len(product_doc_items)):
                    item_data: dict = product_doc_items[index]
                    new_doc_item: DocumentItemModel = create_doc_item(
                        element=item_data,
                        document_id=document.id,
                        user_id=request.user.id,
                    )
                    try:
                        item_balance = DocumentItemBalanceModel.active_objects().get(
                            item_id=item_data['item']['id'],
                        )
                        total_product = item_balance.qty + new_doc_item.qty
                        update_doc_item_balance(
                            total_product=total_product, new_doc_item=new_doc_item,
                            product_item_balance=item_balance
                        )
                    except DocumentItemBalanceModel.DoesNotExist:
                        create_doc_item_balance(
                            user_id=request.user.id,
                            doc_item=new_doc_item
                        )
                    SpiskaModel.objects.filter(
                        item=new_doc_item.item
                    ).delete()
            return res_message(
                message=ResponseMessages.SUCCESS,
                status=status.HTTP_201_CREATED
            )
        except Exception as e:

            return res_error(str(e), status=status.HTTP_400_BAD_REQUEST)


class CreateSellDocument(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request: Request):
        user = request.user

        try:

            doc_type = request.data.get('doc_type')
            product_doc_items = request.data.get('product_doc_items')
            builder_id = request.data.get('builderId')
            debt_data = request.data.get('debt_data')
            is_debt = request.data.get('is_debt')
            with transaction.atomic():
                new_document = create_document(
                    doc_type=doc_type,
                    user=user
                )
                if not is_debt:
                    if builder_id != -1:
                        builder = BuilderModel.objects.get(id=builder_id)
                        if builder is None:
                            return res_message(ResponseMessages.DATA_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)
                        else:
                            create_debt_for_builder(
                                builder_id=builder.id,
                                user_id=user.id,
                                doc_id=new_document.id
                            )
                    if debt_data is not None:
                        create_debt(
                            user_id=user.id,
                            doc_id=new_document.id,
                            name=debt_data['fish'],
                            phone_number=debt_data['phone_number'],
                            phone_number2=debt_data['phone_number2'],
                            address=debt_data['address'],
                            amount=debt_data['amount']
                        )
                else:
                    if builder_id != -1:
                        builder = BuilderModel.active_objects().get(id=builder_id)
                        if builder is None:
                            return res_message(ResponseMessages.DATA_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)
                        else:
                            new_document.builder = builder
                            new_document.save()
                for item in range(len(product_doc_items)):
                    item_data = product_doc_items[item]

                    create_doc_item(
                        element=item_data,
                        document_id=new_document.id,
                        user_id=user.id
                    )
                    sold_item: DocumentItemBalanceModel = DocumentItemBalanceModel.active_objects().get(
                        item_id=item_data['item']['id']
                    )
                    if sold_item:
                        total_product = sold_item.qty - item_data['qty']
                        if total_product != 0:
                            sold_item.qty = total_product
                            sold_item.save()
                        elif total_product == 0:
                            try:
                                is_exist = SpiskaModel.active_objects().get(
                                    item=sold_item.item
                                )
                            except SpiskaModel.DoesNotExist:
                                SpiskaModel.objects.create(
                                    item=sold_item.item,
                                )
                            sold_item.hard_delete(sold_item.pk)
                    else:
                        return res_error(ResponseMessages.DATA_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)
            return res_message(message=ResponseMessages.SUCCESS, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return res_error(str(e))


class BaseView(GenericAPIView):
    queryset = DocumentModel
    serializer_class = DocumentModelSerializer


class ListView(BaseView, BaseListView):
    def get(self, req):
        return self.get_instances(req)


class SoldItemListView(BaseView):
    permission_classes = (AllowAny,)

    def get(self, req):
        total_income = 0.0

        try:
            documents = self.queryset.active_objects().filter(
                doc_type=DocumentModel.SELL,
            )

            today = now().date()
            list_total_selling_week = [
                {
                    'date': (today - timedelta(days=i)), 'price': 0, 'profit': 0.0
                } for i in range(7)
            ]
            for doc in documents:
                doc_date = doc.created_at.date()

                for total in list_total_selling_week:
                    if total['date'] == doc_date:
                        for item in doc.items.all():
                            item: DocumentItemModel = item
                            total_income += math.ceil(item.income_price * item.qty)
                            if item.discount_price > 0:
                                total['price'] += math.ceil(item.discount_price * item.qty)
                            else:
                                total['price'] += math.ceil(item.selling_price * item.qty)
                        total['profit'] = total['price'] - total_income
            return response_list(
                message=ResponseMessages.SUCCESS,
                lst=list_total_selling_week,
                status=status.HTTP_200_OK
            )

        except Exception as e:
            print(e)
            return res_message(message=ResponseMessages.DATA_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)


class DeleteView(BaseView, BaseDeleteView):

    def delete(self, req, pk):
        try:
            return self.delete_instance(req, pk)
        except Exception as e:
            return res_error(str(e))
