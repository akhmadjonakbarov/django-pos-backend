from ..models import CategoryModel
from ..serializers.common_serializers import CategoryModelSerializer

from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.generics import GenericAPIView

from ...base_app.views import BaseAddView, BaseDeleteView, BaseListView, BaseUpdateView
from ...utils.response_type import res_error


class BaseView(GenericAPIView):
    queryset = CategoryModel
    serializer_class = CategoryModelSerializer


class ListView(BaseView, BaseListView):
    def get(self, req):
        try:
            return self.get_instances(req)
        except Exception as e:
            return res_error(str(e))


class AddView(BaseView, BaseAddView):

    def post(self, request):
        try:
            return self.create_instance(request)
        except Exception as e:
            return res_error(str(e))


class UpdateView(BaseView, BaseUpdateView):
    permission_classes = (IsAuthenticated,)

    def patch(self, request, pk):
        return self.update_instance(request, pk)


class DeleteView(BaseView, BaseDeleteView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, pk):
        return self.delete_instance(request, pk)
