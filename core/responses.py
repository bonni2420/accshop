from rest_framework.response import Response
from rest_framework import status


def success_response(
        message: str = "Thao tác thành công", data: dict | None = None, http_status: int = status.HTTP_200_OK
    ):
    payload = {"status": "success", "message": message}
    if data is not None:
        payload["data"] = data
    return Response(payload, status=http_status)


def error_response(
        message: str = "Đã xảy ra lỗi", errors: dict | None = None, http_status: int = status.HTTP_400_BAD_REQUEST
    ):
    payload = {"status": "error", "message": message}
    if errors:
        payload["errors"] = errors
    return Response(payload, status=http_status)
