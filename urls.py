from django.urls import path
from . import views

"main page"
urlpatterns = [
    path('', views.home, name='home'),
    path ('Student',views.LogIn_Student,name='Student')
 ]
urlpatterns =[
    path ('Teacher',views.LogIN_M,name='Teacher')
]
urlpatterns =[
    path ('Dean of Student office',views.LogIn_D,name='Dean of Student office')
]