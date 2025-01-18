from django.urls import path
from newapp import views


urlpatterns = [
    path('first_login/', views.first_login, name='first_login'),  # صفحة تسجيل الدخول
    path('login_M/', views.login, name='login_M'),  # صفحة تسجيل الدخول
    path('Teacherpage/<int:user_id>/', views.Teacherpage, name='Teacherpage'),  # صفحة المعلم
]