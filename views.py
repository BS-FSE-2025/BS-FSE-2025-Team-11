from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

# Verify login details
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  
            return redirect('home')  # Redirect user to page after login
        else:
            messages.error(request, "Invalid username or password")  # error 
    return render(request, 'login.html')  

#---------------------------------------------------------------------#
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Request

@login_required
def student_requests(request):
    requests = Request.objects.filter(student=request.user)
    return render(request, "student_requests.html", {"requests": requests})

@login_required
def dean_requests(request):
    if request.user.is_staff:  # 
        requests = Request.objects.all()
        return render(request, "dean_requests.html", {"requests": requests})
    else:
        return redirect("student_requests")  


@login_required
def update_request(request, request_id):
    if request.method == "POST" and request.user.is_staff:  
        req = get_object_or_404(Request, id=request_id)
        req.status = request.POST.get("status")
        req.remarks = request.POST.get("remarks")
        req.save()
        return redirect("dean_requests")
    else:
        return redirect("student_requests")

from django.shortcuts import render

# الصفحة الرئيسية
def home(request):
    return render(request, 'home.html')

# تسجيل دخول الطالب
def LogIn_Student(request):
    return render(request, 'student_login.html')

# تسجيل دخول المعلم
def LogIN_M(request):
    return render(request, 'teacher_login.html')

# تسجيل دخول مكتب عمادة شؤون الطلاب
def LogInDeanStu(request):
    return render(request, 'LogInDeanStu.html')
