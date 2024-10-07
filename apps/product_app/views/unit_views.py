from ..models import UnitModel
from ..serializers.common_serializers import UnitModelSerializer

from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.generics import GenericAPIView

from ...base_app.views import BaseListView, BaseUpdateView, BaseDeleteView, BaseAddView


class BaseView(GenericAPIView):
    queryset = UnitModel
    serializer_class = UnitModelSerializer


class ListView(BaseView, BaseListView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, req):
        return self.get_instances(req)


class AddView(BaseView, BaseAddView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        return self.create_instance(request)


class UpdateView(BaseView, BaseUpdateView):
    permission_classes = [IsAuthenticated, ]

    def patch(self, request, pk):
        return self.update_instance(request, pk)


class DeleteView(BaseView, BaseDeleteView):
    permission_classes = [IsAuthenticated, ]

    def delete(self, request, pk):
        return self.delete_instance(request, pk)
