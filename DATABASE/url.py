from django.urls import path
from . import views

urlpatterns = [
    path('first-login/', views.first_login, name='first_login'),
]
