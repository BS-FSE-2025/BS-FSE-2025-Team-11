from django.shortcuts import render
from django.http import HttpResponse
from .models import User
from django.contrib.auth.hashers import make_password

def first_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = make_password(request.POST['password'])  # تشفير كلمة المرور
        email = request.POST['email']
        phone_number = request.POST.get('phone_number', '')
        id_number = request.POST.get('id_number', '')
        specialization = request.POST.get('specialization', '')

        # حفظ البيانات في قاعدة البيانات
        user = User(
            username=username,
            password=password,
            email=email,
            phone_number=phone_number,
            id_number=id_number,
            specialization=specialization,
        )
        user.save()

        return HttpResponse("User added successfully!")

    return render(request, 'first_login.html')
