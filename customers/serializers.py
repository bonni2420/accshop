import re
from rest_framework import serializers
from .models import Customer
from datetime import date


class BaseCustomerSerializer(serializers.ModelSerializer):
    def validate_name(self, value):
        if not re.match(r"^[A-Za-zÀ-ỹ\s']+$", value.strip()):
            raise serializers.ValidationError("Họ tên chỉ được chứa chữ cái và khoảng trắng")
        return value.strip()

    def validate_username(self, value):
        if not re.match(r'^[A-Za-z0-9]+$', value):
            raise serializers.ValidationError("Username chỉ được chứa chữ và số, không có ký tự đặc biệt")
        if ' ' in value:
            raise serializers.ValidationError("Username không được chứa khoảng trắng")
        return value

    def validate_phone(self, value):
        if not value.isdigit() or len(value) < 8 or len(value) > 15:
            raise serializers.ValidationError("Số điện thoại không hợp lệ")
        return value


class RegisterSerializer(BaseCustomerSerializer):
    """Đăng ký tài khoản mới."""
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={'input_type': 'password'},
        error_messages={'min_length': "Mật khẩu phải có ít nhất 8 ký tự"},
    )

    class Meta:
        model = Customer
        fields = ['name', 'phone', 'username', 'password']
        extra_kwargs = {
            'phone': {'validators': []},
            'username': {'validators': []},
        }

    def create(self, validated_data):
        user = Customer(**validated_data)
        user.save(force_insert=True)
        return user


class LoginSerializer(serializers.Serializer):
    """Đăng nhập bằng username hoặc phone + password."""
    username_or_phone = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, attrs):
        username_or_phone = attrs.get('username_or_phone', '').strip()
        password = attrs.get('password')

        if not username_or_phone:
            raise serializers.ValidationError({"username_or_phone": "Vui lòng nhập username hoặc số điện thoại."})
        if not password:
            raise serializers.ValidationError({"password": "Vui lòng nhập mật khẩu."})
        return attrs


class CustomerProfileSerializer(serializers.ModelSerializer):
    """Serializer chỉ đọc — dùng để hiển thị thông tin người dùng hiện tại."""
    class Meta:
        model = Customer
        exclude = ["password", "is_delete","is_active"]
        read_only_fields = [field.name for field in Customer._meta.fields if field.name != "id"]


### Có đầy đủ validate tất cả các trường cần thiết,
class CustomerUpdateSerializer(BaseCustomerSerializer):
    class Meta:
        model = Customer
        fields = ["username","email","phone","name"]
        extra_kwargs = {
            "username": {"validators": []},
            "email": {"validators": []},
            "phone": {"validators": []},
        }

    def validate_email(self, value):
        if value:
            value = value.strip()
            email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
            if not re.match(email_regex, value):
                raise serializers.ValidationError("Email không hợp lệ")
        return value
