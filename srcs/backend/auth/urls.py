from django.urls import path 
from . import views 
urlpatterns = [
    path('verify_mfa/', views.verify_mfa, name='verify_mfa'),
    path('disable-2fa/', views.disable_2fa, name='disable_2fa'),
]