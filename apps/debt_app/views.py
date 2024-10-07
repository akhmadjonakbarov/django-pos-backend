from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from apps.base_app.views import BaseListView, BaseAddView, BaseUpdateView, BaseDeleteView
from .models import DebtModel
from .serializers import DebtModelSerializer
from ..utils.response_messages import ResponseMessages
from ..utils.response_type import response_list, res_message


class BaseView(GenericAPIView):
    queryset = DebtModel
    serializer_class = DebtModelSerializer


class ListView(BaseView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request):
        un_paid_debts = self.queryset.objects.filter(is_paid=False, builder_id=None)
        serializer = self.serializer_class(un_paid_debts, many=True)
        return response_list(lst=serializer.data)


class AddView(BaseView, BaseAddView):

    def post(self, request):
        return self.create_instance(request)


class UpdateView(BaseView, BaseUpdateView):
    def patch(self, request, pk):
        return self.update_instance(request, pk)


class DeleteView(BaseView, BaseDeleteView):
    def delete(self, request, pk):
        return self.delete_instance(request, pk)


class PayDebtView(BaseView):
    permission_classes = (IsAuthenticated,)

    def patch(self, request, pk):
        debt = self.queryset.objects.get(id=pk)
        debt.is_paid = True
        debt.save()
        return res_message(status=status.HTTP_200_OK, message=ResponseMessages.SUCCESS)
