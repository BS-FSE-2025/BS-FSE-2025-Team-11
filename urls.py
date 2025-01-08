from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), 
    path('Student/', views.login, name='Student'),  
    path('Teacher/', views.login_M, name='Teacher'),  
    path('Dean-of-Student-office/', views.LogInDeanStu, name='Dean_of_Student_office') 
]
