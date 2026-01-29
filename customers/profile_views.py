from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db import transaction, IntegrityError
from django.contrib.auth.hashers import check_password, make_password

from core.db_exceptions import handle_integrity_error
from core.auth_customer import CustomJWTAuthentication
from core.responses import success_response, error_response
from customers.serializers import CustomerProfileSerializer, CustomerUpdateSerializer
from .models import Customer


class InforCustomer(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]

    def get(self, request):        
        user = (
            Customer.objects
            .defer('password', "is_active", "is_delete")
            .get(id=request.user.id)
        )
        
        serializer = CustomerProfileSerializer(user)

        return success_response(
            "Lấy Thông Tin của Quý Khách Thành Công (DB)",
            data=serializer.data
        )


class UpdateCustomer(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]

    @transaction.atomic
    def patch(self, request):
        try:
            customer = Customer.objects.get(id=request.user.id, is_active=True)
            serializer = CustomerUpdateSerializer(customer, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        except IntegrityError as e:
            err_info = handle_integrity_error(e)
            return error_response(err_info["message"], errors=err_info["errors"])
        except Customer.DoesNotExist:
            return error_response("Không tìm thấy khách hàng", http_status=status.HTTP_404_NOT_FOUND)

        return success_response("Cập nhật thông tin khách hàng thành công")


class UpdatePasswordCustomer(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]

    def patch(self, request):
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not old_password or not new_password:
            return error_response("Vui lòng điền đầy đủ old_password và new_password")

        if len(new_password) < 8:
            return error_response("Mật khẩu mới phải có ít nhất 8 ký tự")

        user_pw = Customer.objects.filter(id=request.user.id).values_list("password", flat=True).first()
        if not user_pw or not check_password(old_password, user_pw):
            return error_response("Mật khẩu cũ không đúng")

        new_password = make_password(new_password)
        Customer.objects.filter(id=request.user.id).update(password=new_password)

        return success_response("Đổi mật khẩu thành công")