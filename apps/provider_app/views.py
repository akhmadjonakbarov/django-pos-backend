from rest_framework.generics import GenericAPIView
from apps.base_app.views import BaseAddView, BaseDeleteView, BaseListView, BaseUpdateView
from apps.provider_app.models import ProviderModel
from apps.provider_app.serializers import ProviderModelSerializer


class BaseView(GenericAPIView):
    queryset = ProviderModel
    serializer_class = ProviderModelSerializer


class ListView(BaseView, BaseListView):

    def get(self, req):
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
