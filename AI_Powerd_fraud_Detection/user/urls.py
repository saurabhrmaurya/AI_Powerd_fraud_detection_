from django.urls import path
from .views import register_view, login_view, logout_view,verify_otp

from dashboard.views import dashboard_view

urlpatterns = [
    path('', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('verify_otp/', verify_otp, name='verify_otp'),
]
