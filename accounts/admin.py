from django.contrib import admin
from django.utils.html import format_html
from .models import Category, GameAccount, GameAccountImage


class GameAccountImageInline(admin.StackedInline):
    model = GameAccountImage
    extra = 1
    min_num = 0
    fields = ("image_preview", "image")
    readonly_fields = ("image_preview",)
    
    @admin.display(description="Xem trước ảnh")
    def image_preview(self, obj):
        if obj.pk and obj.image:
            return format_html(
                '<img src="{}" style="height:120px;border-radius:6px;" />',
                obj.image.url
            )
        return "—"

    image_preview.short_description = "Xem trước ảnh"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")
    search_fields = ("name",)
    ordering = ("id",)
    list_display_links = ["id","name"]
    list_per_page = 20


@admin.register(GameAccount)
class GameAccountAdmin(admin.ModelAdmin):
    list_display = (
        "id","name","username","category","price",
        "stock","is_sold","thumbnail_preview",
    )
    list_filter = ("category","is_sold")
    search_fields = ("name","username","email","phone_number")
    readonly_fields = (
        "thumbnail_preview",
        "created_at",
        "updated_at",
    )
    list_display_links = ("name",)
    
    fieldsets = (
        ("Thông tin chung", {
            "fields": (
                "name",
                "category",
                "thumbnail_preview",
                "thumbnail",
                "description",
                "price",
                "stock",
            )
        }),
        ("Thông tin tài khoản", {
            "fields": (
                "username",
                "password",
                "phone_number",
                "email",
                "is_sold",
            )
        }),
        ("Thời gian", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )
    list_per_page = 20

    @admin.display(description="Ảnh đại diện")
    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html(
                '<img src="{}" style="height:120px;border-radius:6px;" />',
                obj.thumbnail.url
            )
        return "—"

    thumbnail_preview.short_description = "Ảnh đại diện"

    inlines = [GameAccountImageInline]
