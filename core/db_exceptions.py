from django.db import IntegrityError


def handle_integrity_error(error: IntegrityError) -> dict:
    try:
        err_msg = str(error).lower()

        if "username" in err_msg:
            return {
                "message": "Vui lòng chọn Tên Đăng Nhập khác",
                "errors": {"username": "Tên Đăng Nhập đã tồn tại."},
            }
        elif "phone" in err_msg:
            return {
                "message": "Vui lòng chọn Số Điện Thoại khác",
                "errors": {"phone": "Số Điện Thoại đã được sử dụng"},
            }
        elif "email" in err_msg:
            return {
                "message": "Vui lòng chọn Email khác",
                "errors": {"email": "Email đã tồn tại"},
            }
        else:
            return {
                "message": "Lỗi dữ liệu không hợp lệ",
                "errors": {"non_field_errors": "Lỗi dữ liệu không hợp lệ"},
            }

    except Exception:
        return {
            "message": "Đã xảy ra lỗi nội bộ khi xử lý dữ liệu",
            "errors": {"non_field_errors": "Lỗi không xác định"},
        }