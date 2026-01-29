from django.http import JsonResponse
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework import status
from rest_framework.exceptions import (
    ValidationError,
    AuthenticationFailed,
    NotAuthenticated
)
from django.http import Http404
from django.urls.exceptions import Resolver404

from .responses import error_response


def custom_exception_handler(exc, context):
    """
    Custom exception handler toàn hệ thống (DRF)
    Chỉ trả về lỗi đơn giản, đồng nhất format
    """
    response = drf_exception_handler(exc, context)

    # 404 URL không tồn tại
    if isinstance(exc, (Http404, Resolver404)):
        return error_response(
            message="Đường dẫn API không tồn tại",
            http_status=status.HTTP_404_NOT_FOUND,
        )

    # 405 Method Not Allowed
    if response is not None and response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED:
        return error_response(
            message="Phương thức này không được phép tại endpoint hiện tại",
            http_status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    # Chưa đăng nhập
    if isinstance(exc, NotAuthenticated):
        return error_response(
            message="Bạn cần đăng nhập để thực hiện hành động này",
            http_status=status.HTTP_401_UNAUTHORIZED,
        )

    # Token hết hạn hoặc không hợp lệ
    if isinstance(exc, AuthenticationFailed):
        return error_response(
            message="Token không hợp lệ hoặc đã hết hạn. Vui lòng đăng nhập lại",
            http_status=status.HTTP_401_UNAUTHORIZED,
        )

    # ValidationError (serializer)
    if isinstance(exc, ValidationError):
        return error_response(
            message="Dữ liệu gửi lên không hợp lệ",
            http_status=status.HTTP_400_BAD_REQUEST,
        )

    # Nếu DRF xử lý được exception
    if response is not None:
        return error_response(
            message=response.data.get("detail", "Đã xảy ra lỗi không xác định"),
            http_status=response.status_code,
        )

    # Lỗi không xác định
    return error_response(
        message="Lỗi máy chủ nội bộ.",
        http_status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


def custom_404_handler(request, exception=None):
    """Handler riêng cho 404 ở mức Django (ngoài DRF)"""
    return JsonResponse(
        {
            "status": "error",
            "message": "Đường dẫn API không tồn tại",
        },
        status=404
    )