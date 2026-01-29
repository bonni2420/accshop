from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework.exceptions import AuthenticationFailed as DRFAuthFailed
from django.db import DatabaseError, OperationalError

from customers.models import Customer


class CustomJWTAuthentication(JWTAuthentication):
    """
    Custom JWT Authentication cho Customer:
    - Chỉ dùng user_id trong token
    - Chặn user bị soft delete / inactive
    - Chuẩn hóa error response
    """

    def get_validated_token(self, raw_token):
        try:
            return super().get_validated_token(raw_token)
        except InvalidToken:
            raise DRFAuthFailed({
                "status": "error",
                "message": "Token không hợp lệ hoặc đã hết hạn. Vui lòng đăng nhập lại.",
            })
        except Exception:
            raise DRFAuthFailed({
                "status": "error",
                "message": "Lỗi không xác định khi xác thực token.",
            })

    def get_user(self, validated_token):
        """
        Lấy Customer từ token.
        Token chỉ chứa user_id.
        """
        user_id = validated_token.get("id")
        if not user_id:
            raise DRFAuthFailed({
                "status": "error",
                "message": "Token không hợp lệ (thiếu id).",
            })

        try:
            user = Customer.objects.get(
                id=user_id,
                is_delete=False,
                is_active=True
            )
        except Customer.DoesNotExist:
            raise DRFAuthFailed({
                "status": "error",
                "message": "Tài khoản không tồn tại hoặc đã bị vô hiệu hóa.",
            })
        except (DatabaseError, OperationalError):
            raise DRFAuthFailed({
                "status": "error",
                "message": "Lỗi hệ thống khi xác thực người dùng.",
            })

        return user
