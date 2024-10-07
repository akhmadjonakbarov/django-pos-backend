from rest_framework import status
from rest_framework.request import Request

from ..models import ItemModel, CategoryModel, CompanyModel, UnitModel
from ..serializers.common_serializers import ItemModelSerializer

from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.generics import GenericAPIView

from ...base_app.views import BaseListView, BaseUpdateView, BaseDeleteView, BaseAddView

from ...utils.response_type import res_error, response_item


class BaseItemView(GenericAPIView):
    queryset = ItemModel
    serializer_class = ItemModelSerializer

    def get_item_data(self, request):
        category_data: dict = request.data.get('category')
        company_data: dict = request.data.get('company')
        unit_data: dict = request.data.get('unit')

        # Fetch the related models
        category = CategoryModel.objects.get(id=category_data.get('id'))
        company = CompanyModel.objects.get(id=company_data.get('id'))
        unit = UnitModel.objects.get(id=unit_data.get('id'))

        # Return the cleaned data
        return {
            "category": category,
            "company": company,
            "name": request.data.get('name'),
            "barcode": request.data.get('barcode'),
            "unit": unit,
            "user": request.user
        }


class ItemListView(BaseItemView, BaseListView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, req):
        return self.get_instances(req)


class ItemAddView(BaseItemView, BaseAddView):

    def post(self, request: Request):
        try:
            item_data = self.get_item_data(request)
            item = ItemModel.objects.create(**item_data)
            return response_item(item=self.serializer_class(item).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return res_error(error=str(e))


class ItemUpdateView(BaseItemView, BaseUpdateView):

    def patch(self, request, pk):
        try:
            # Fetch the existing item
            item = ItemModel.objects.get(id=pk)

            # Use the shared method to get updated item data
            item_data = self.get_item_data(request)

            # Update the item's attributes
            for attr, value in item_data.items():
                setattr(item, attr, value)

            item.save()

            return response_item(item=self.serializer_class(item).data, status=status.HTTP_200_OK)
        except Exception as e:
            return res_error(error=str(e))


class ItemDeleteView(BaseItemView, BaseDeleteView):

    def delete(self, request, pk):
        return self.delete_instance(request, pk)
