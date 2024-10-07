from rest_framework.response import Response
from rest_framework import status as status_codes
from .response_messages import ResponseMessages


def response_list(lst, message=ResponseMessages.SUCCESS, status=status_codes.HTTP_200_OK) -> Response:
    return Response({
        'data': {
            'message': message,
            'list': lst
        }
    }, status=status)


def response_item(item, message=ResponseMessages.SUCCESS, status=status_codes.HTTP_200_OK) -> Response:
    return Response({
        'data': {
            'message': message,
            'item': item
        }
    }, status=status)


def res_error(error, status=status_codes.HTTP_400_BAD_REQUEST) -> Response:
    return Response({
        'data': {
            'error': error,
        }
    }, status=status)  # You can set the status code as needed


def res_message(message, status=status_codes.HTTP_400_BAD_REQUEST) -> Response:
    return Response({
        'data': {
            'message': message,
        }
    }, status=status)
