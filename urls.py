from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # الصفحة الرئيسية
    path('Student/', views.LogIn_Student, name='Student'),  # تسجيل دخول الطالب
    path('Teacher/', views.LogIN_M, name='Teacher'),  # تسجيل دخول المعلم
    path('Dean-of-Student-office/', views.LogInDeanStu, name='Dean_of_Student_office')  # تسجيل دخول مكتب عمادة شؤون الطلاب
]
