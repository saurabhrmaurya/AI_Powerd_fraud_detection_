from django.urls import path
from .views import dashboard_view
from user.views import logout_view

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('logout/', logout_view, name='logout' ),      
]
