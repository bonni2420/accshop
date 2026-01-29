from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny

from .models import GameAccount, Category
from .serializers import (
    GameAccountListSerializer,
    GameAccountDetailSerializer,
    CategorySimpleSerializer
)
from .filters import GameAccountFilter
from .pagination import GameAccountPagination


class GameAccountListAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    
    queryset = GameAccount.objects.select_related("category").prefetch_related("images")
    serializer_class = GameAccountListSerializer
    pagination_class = GameAccountPagination

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = GameAccountFilter
    ordering_fields = ["price", "created_at"]
    ordering = ["-created_at"]


class GameAccountDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    
    queryset = GameAccount.objects.select_related("category").prefetch_related("images")
    serializer_class = GameAccountDetailSerializer

class CategoryListAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = CategorySimpleSerializer

    def get_queryset(self):
        return (
            Category.objects
            .filter(gameaccount__isnull=False)
            .distinct()
        )