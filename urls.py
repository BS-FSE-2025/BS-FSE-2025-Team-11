"""
URL configuration for newproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from newapp import views
from django.contrib.auth import views as auth_views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'), 
    path('Sign_up.html', views.Signup, name='Sign_up'),
    path('first_login.html', views.first_login, name='first_login'), 
    path('login_S.html', views.login_S, name='login_S'), 
    path('login_M.html', views.login_M, name='login_M'),
    path('Teacherpage.html', views.Teacherpage, name='Teacherpage'), 
    path('Studentpage.html', views.Studentpage, name='Studentpage'),
    path('delete_group_request/<int:request_id>/', views.delete_group_request_view, name='delete_group_request'),
    path('delete_private_request/<int:request_id>/', views.delete_private_request_view, name='delete_private_request'),
    path('Group_Diary.html', views.Group_Diary, name='Group_Diary'),
    path('private_Diary.html', views.private_Diary, name='private_Diary'),
    path('private_request.html', views.private_request, name='private_request'),
    path('manager_view.html', views.manager_view, name='manager_view'),
    path('Group_request.html', views.Group_request, name='gruop_request'),  
    path('dean_page.html', views.dean_page, name='dean_page'),
    path('Deanlogin.html', views.Deanlogin, name='Deanlogin'),
    path('najah.hyml', views.najah, name='Najah'),
    path("dean_requests.html", views.dean_requests_view, name="dean_requests"),
    path('request_status.html', views.request_status_view, name='request_status'),
    path('update_user/<int:user_id>/', views.update_user, name='update_user'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('update_time/<int:requset_id>/', views.update_time, name='update_time'),
    path('update_timeG/<int:group_id>/', views.update_timeG, name='update_timeG'),
    path('manage_users.html', views.manage_users, name='manage_users'),
    path('system_Teacher.html', views.system_Teacher_view, name=''),
    path('system_Student.html', views.system_Student_view, name='system_Student'),
    path('admin_dashboard.html', views.admin_dashboard, name=''),
    path('private_diary_view/<int:diary_id>/', views.private_diary_view, name='private_diary_view'),
    path('group_diary_view/<int:group_id>/', views.group_diary_view, name='group_diary_view'),
    path('contactStudent.html', views.contactd_view, name=''),
    path('contD.html', views.contd_view, name=''),
    path('logout/', views.logout, name='logout'),
    path('home.html',views.home,name='home'), 
    
]
    
