from django.contrib import admin
from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "name",
        "phone",
        "balance",
        "is_active",
        "is_delete",
    )
    list_display_links = ("id","username")
    
    list_filter = ("is_active", "is_delete", "created_at")
    search_fields = ("username", "name", "phone", "email")
    ordering = ("-created_at",)
    
    readonly_fields = ("created_at", "updated_at")
    
    fieldsets = (
        ("Thông tin cá nhân", {
            "fields": ("name","phone","email","balance","username","password")
        }),
        ("Trạng thái hệ thống", {
            "fields": ("is_active", "is_delete", "created_at", "updated_at")
        }),
    )
    
    list_per_page = 30
