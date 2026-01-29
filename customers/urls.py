from django.urls import path
from . import auth_views, profile_views

app_name = 'customers'
urlpatterns = [
    path('register', auth_views.RegisterCustomer.as_view(), name='register'),
    path('login', auth_views.LoginCustomer.as_view(), name='login'),
    path('logout', auth_views.LogoutCustomer.as_view(), name='logout'),
    path('refresh-token', auth_views.RefreshTokenCustomer.as_view(), name='refresh-token'),
    
    path('me', profile_views.InforCustomer.as_view(), name='me'),
    path('update', profile_views.UpdateCustomer.as_view(), name='update'),
    path('change-password', profile_views.UpdatePasswordCustomer.as_view(), name='change-password'),
]
