from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.utils import aware_utcnow


class CustomerRefreshToken(RefreshToken):
    @classmethod
    def for_user(cls, customer):
        """
            Tạo refresh token cho khách hàng (Customer).
            Giữ nguyên cấu trúc như for_user gốc của SimpleJWT,
            nhưng không đụng gì đến bảng OutstandingToken.
        """
        if not hasattr(customer, "id"):
            raise TypeError("Đối tượng truyền vào phải là Customer instance hợp lệ")

        token = cls()
        token["id"] = customer.id
        token["username"] = getattr(customer, "username", None)
        token["token_type"] = "refresh"
        token["iat"] = aware_utcnow()

        if hasattr(customer, "email"):
            token["email"] = customer.email
        if hasattr(customer, "phone"):
            token["phone"] = customer.phone

        return token

    @classmethod
    def for_customer(cls, customer):
        return cls.for_user(customer)