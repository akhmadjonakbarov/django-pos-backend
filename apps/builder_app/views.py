from rest_framework import status
from rest_framework.permissions import AllowAny

from .models import BuilderModel
from .serializers import BuilderModelSerializer

from rest_framework.generics import GenericAPIView

from apps.base_app.views import BaseAddView, BaseDeleteView, BaseListView, BaseUpdateView
from ..debt_app.models import DebtModel
from ..debt_app.serializers import DebtModelSerializer
from ..statistic_app.models import StatisticsModel
from ..utils.response_messages import ResponseMessages
from ..utils.response_type import response_list


class BaseView(GenericAPIView):
    queryset = BuilderModel
    serializer_class = BuilderModelSerializer


class ListView(BaseView, BaseListView):
    def get(self, req):
        StatisticsModel.objects.update_or_create(
            name="builders",
            defaults={
                'value': self.queryset.active_objects().count()
            }
        )
        return self.get_instances(req)


class AddView(BaseView, BaseAddView):
    def post(self, request):
        return self.create_instance(request)


class UpdateView(BaseView, BaseUpdateView):
    def patch(self, request, pk):
        return self.update_instance(request, pk)


class DeleteView(BaseView, BaseDeleteView):
    def delete(self, request, pk):
        return self.delete_instance(request, pk)


class ListBuildeDebtView(GenericAPIView):
    queryset = DebtModel
    serializer_class = None
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        un_paid_debts = self.queryset.objects.filter(builder_id=pk, is_paid=False)
        serializer = self.serializer_class(un_paid_debts, many=True)
        return response_list(
            message=ResponseMessages.SUCCESS,
            lst=serializer.data, status=status.HTTP_200_OK
        )


class ListBuilderDebtView(GenericAPIView):
    queryset = DebtModel
    serializer_class = DebtModelSerializer
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        un_paid_debts = self.queryset.objects.filter(builder_id=pk, is_paid=False)
        serializer = self.serializer_class(un_paid_debts, many=True)
        return response_list(
            message=ResponseMessages.SUCCESS,
            lst=serializer.data, status=status.HTTP_200_OK
        )
