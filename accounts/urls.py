from django.urls import path
from .views import GameAccountListAPIView, GameAccountDetailAPIView, CategoryListAPIView

app_name = 'accounts'
urlpatterns = [
    path("", GameAccountListAPIView.as_view()),
    path("<int:pk>/", GameAccountDetailAPIView.as_view()),
    path("categories/", CategoryListAPIView.as_view()),
]
