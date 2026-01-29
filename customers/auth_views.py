from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from django.db.models import Q
from django.db import IntegrityError, DatabaseError, transaction
from django.conf import settings

from core.db_exceptions import handle_integrity_error
from core.auth_customer import CustomJWTAuthentication
from core.tokens import CustomerRefreshToken
from core.responses import success_response, error_response
from .serializers import RegisterSerializer, LoginSerializer
from .models import Customer

refresh_lifetime = int(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds())


class RegisterCustomer(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(
                message="Dữ liệu không hợp lệ",
                errors=serializer.errors,
                http_status=status.HTTP_400_BAD_REQUEST
            )

        try:
            with transaction.atomic():
                user = serializer.save()

        except IntegrityError as e:
            err_info = handle_integrity_error(e)
            return error_response(
                message=err_info["message"],
                errors=err_info["errors"],
                http_status=status.HTTP_400_BAD_REQUEST
            )

        except DatabaseError:
            return error_response(
                message="Lỗi hệ thống cơ sở dữ liệu",
                http_status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return success_response(
            message="Đăng ký tài khoản thành công",
            http_status=status.HTTP_201_CREATED
        )


class LoginCustomer(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(
                message="Dữ liệu không hợp lệ.",
                errors=serializer.errors,
                http_status=status.HTTP_400_BAD_REQUEST
            )

        username_or_phone = serializer.validated_data["username_or_phone"]
        password = serializer.validated_data["password"]

        user = Customer.objects.filter(
            Q(username__iexact=username_or_phone) | Q(phone=username_or_phone)
        ).only("id", "username", "phone", "password", "is_active", "is_delete").first()

        if not user or user.is_delete or not user.is_active:
            return error_response(
                message="Tài khoản không tồn tại hoặc đã bị khóa",
                http_status=status.HTTP_403_FORBIDDEN
            )

        if not user.check_password(password):
            return error_response(
                message="Tên đăng nhập hoặc mật khẩu không đúng",
                http_status=status.HTTP_400_BAD_REQUEST
            )

        refresh = CustomerRefreshToken.for_user(user)
        access = refresh.access_token

        response = success_response(
            message="Đăng nhập thành công",
            data={"access": str(access)},
            http_status=status.HTTP_200_OK
        )

        response.set_cookie(
            key="refresh",
            value=str(refresh),
            httponly=True,
            secure=True,
            samesite="None",
            max_age=refresh_lifetime,
            path="/",
        )
        return response


class LogoutCustomer(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh")
        if not refresh_token:
            return error_response(
                message="Cần có Refresh token",
                http_status=status.HTTP_400_BAD_REQUEST
            )

        try:
            RefreshToken(refresh_token).blacklist()
        except TokenError:
            return error_response(
                message="Refresh token không hợp lệ hoặc đã hết hạn",
                http_status=status.HTTP_400_BAD_REQUEST
            )

        return success_response(
            message="Đăng xuất thành công",
            http_status=status.HTTP_200_OK
        )


class RefreshTokenCustomer(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh")
        if not refresh_token:
            return error_response(
                message="Thiếu refresh token trong cookie",
                http_status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = CustomerRefreshToken(refresh_token)
            new_access = token.access_token

            response = success_response(
                message="Tạo Access Token mới thành công",
                data={"access": str(new_access)},
                http_status=status.HTTP_200_OK
            )

            response.set_cookie(
                key="refresh",
                value=str(refresh_token),
                httponly=True,
                secure=True,
                samesite="None",
                max_age=refresh_lifetime,
                path="/",
            )
            return response

        except (InvalidToken, TokenError):
            return error_response(
                message="Refresh token không hợp lệ hoặc đã hết hạn",
                http_status=status.HTTP_401_UNAUTHORIZED
            )

        except Exception:
            return error_response(
                message="Lỗi không xác định khi làm mới token",
                http_status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
