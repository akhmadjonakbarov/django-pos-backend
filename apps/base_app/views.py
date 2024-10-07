from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework import status

from apps.base_app.models import BaseModel
from apps.utils.response_messages import ResponseMessages
from apps.utils.response_type import response_item, res_error, response_list


class BaseListView(GenericAPIView):
    queryset = None
    serializer_class = None
    permission_classes = (AllowAny,)

    def get_instances(self, request):
        objects = self.get_queryset().active_objects()
        serializer = self.get_serializer(objects, many=True)
        return response_list(lst=serializer.data)


class BaseAddView(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = None
    queryset = None

    def create_instance(self, request):
        """Shared method for creating an instance"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response_item(message='success', item=serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return res_error(error=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BaseUpdateView(GenericAPIView):
    queryset = None
    serializer_class = None
    permission_classes = [IsAuthenticated, ]

    def update_instance(self, request, pk):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = self.get_queryset().objects.get(id=pk)  # Use model class to retrieve object
            serializer.update(instance, serializer.validated_data)
            return response_item(message=ResponseMessages.SUCCESS, item=serializer.data, status=status.HTTP_200_OK)

        return res_error(error=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BaseDeleteView(GenericAPIView):
    queryset = BaseModel
    serializer_class = None
    permission_classes = [IsAuthenticated, ]

    def delete_instance(self, request, pk):
        """Shared method for deleting an instance"""
        try:
            obj = self.queryset.objects.get(id=pk)  # Use model class to retrieve object
            obj.delete()
            return response_item(
                message='success', item=self.get_serializer(obj, many=False).data,
                status=status.HTTP_200_OK,
            )
        except self.queryset.DoesNotExist:
            return res_error(error=f'Object with id {pk} does not exist', status=status.HTTP_404_NOT_FOUND)
