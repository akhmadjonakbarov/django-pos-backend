from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.generics import GenericAPIView

from apps.spiska_app.models import SpiskaModel
from .serializers import SpiskaModelSerializer
from ..base_app.views import BaseListView


class BaseView(GenericAPIView):
    queryset = SpiskaModel
    serializer_class = SpiskaModelSerializer


class ListView(BaseView, BaseListView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, req):
        return self.get_instances(req)
