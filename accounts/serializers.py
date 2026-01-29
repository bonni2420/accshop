from rest_framework import serializers
from .models import Category, GameAccount, GameAccountImage


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description"]


class GameAccountImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameAccountImage
        fields = ["id", "image"]
        
class CategorySimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class GameAccountListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    thumbnail = serializers.ImageField(read_only=True)

    class Meta:
        model = GameAccount
        fields = [
            "id",
            "name",
            "category",
            "thumbnail",
            "price",
            "stock",
            "is_sold",
        ]


class GameAccountDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    images = GameAccountImageSerializer(many=True, read_only=True)

    class Meta:
        model = GameAccount
        fields = [
            "id",
            "name",
            "category",
            "thumbnail",
            "images",
            "description",
            "price",
            "stock",
            "username",
            "email",
            "phone_number",
            "is_sold",
            "created_at",
        ]
