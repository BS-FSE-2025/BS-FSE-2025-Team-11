from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse
from django.shortcuts import  get_object_or_404
from django.forms import modelformset_factory
from .forms import PersonalRequestForm


def home(request):
    return render(request, 'home.html')
def Teacherpage(request):
    return render(request, 'Teacherpage.html')
def Group_Diary(request):
    return render(request, 'Group_Diary.html')
def private_Diary(request):
    return render(request, 'private_Diary.html')
def Studentpage(request):
    return render(request, 'Studentpage.html')
def Update_time(request):
    return render(request, 'Update_time.html') 

def first_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')
        id_number = request.POST.get('id_number')
        specialization = request.POST.get('specialization')

        # التحقق من وجود المستخدم مسبقًا
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please log in.')
            return redirect('login_M')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists. Please log in.')
            return redirect('login_M')

        # إنشاء مستخدم جديد
        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password),  # تشفير كلمة المرور
            phone_number=phone_number,
            id_number=id_number,
            specialization=specialization,
        )

        # تسجيل دخول المستخدم تلقائيًا
        login(request, user)
        messages.success(request, 'Account successfully created.')
        return redirect('Teacherpage')

    return render(request, 'first_login.html')


# Login function


def login_M(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # التحقق من صحة بيانات تسجيل الدخول
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # تسجيل دخول المستخدم
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('Teacherpage')  # توجيه إلى صفحة Teacherpage
        else:
            # إذا كانت البيانات خاطئة
            messages.error(request, 'Invalid username or password.')
            return redirect('login_M')

    # عرض صفحة تسجيل الدخول في حالة الطلب GET
    return render(request, 'login_M.html')

def Signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')
        id_number = request.POST.get('id_number')
        specialization = request.POST.get('specialization')

        # التحقق من وجود المستخدم مسبقًا
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please log in.')
            return redirect('login_S')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists. Please log in.')
            return redirect('login_S')

        # إنشاء مستخدم جديد
        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password),  # تشفير كلمة المرور
            phone_number=phone_number,
            id_number=id_number,
            specialization=specialization,
        )

        # تسجيل دخول المستخدم تلقائيًا
        login(request, user)
        messages.success(request, 'Account successfully created.')
        return redirect('Studentpage')

    return render(request, 'Sign_up.html')


# Login function

def login_S(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # التحقق من صحة بيانات تسجيل الدخول
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # تسجيل دخول المستخدم
            login(request, user)
            messages.success(request, f'Welcome, {user.username}!')
            return redirect('Studentpage')  
        else:
            # إذا كانت البيانات خاطئة
            messages.error(request, 'Invalid username or password.')
            return redirect('login_S')

    # عرض صفحة تسجيل الدخول في حالة الطلب GET
    return render(request, 'login_S.html') 

# عرض جميع المستخدمين (اختبار)
def test_view(request):
    records = User.objects.all()  # استرداد جميع السجلات
    return render(request, 'test_view.html', {'records': records})


# اختبار الاتصال بقاعدة البيانات
def check_database_connection(request):
    from django.db import connection

    try:
        # تنفيذ استعلام بسيط لاختبار الاتصال
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return JsonResponse({"status": "success", "message": "Database is connected!"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})




from django.shortcuts import render, redirect
from .forms import DiaryGroupForm
from .models import DiaryGroup, DiaryStudent

# في views.py
def Group_Diary(request):
    if request.method == 'POST':
        group_form = DiaryGroupForm(request.POST)
        if group_form.is_valid():
            group = group_form.save()
            students = []
            student_names = request.POST.getlist('student-name[]')
            attendance_dates = request.POST.getlist('student-date[]')
            attendance_hours = request.POST.getlist('student-hours[]')

            for i in range(len(student_names)):
                student_name = student_names[i]
                attendance_date = attendance_dates[i]
                attendance_hours = attendance_hours[i]
                
                if student_name and attendance_date and attendance_hours:
                    students.append(DiaryStudent(
                        group=group,
                        student_name=student_name,
                        attendance_date=attendance_date,
                        attendance_hours=attendance_hours
                    ))
            if students:
                DiaryStudent.objects.bulk_create(students)
            return redirect('Teacherpage')
        else:
            print("Form errors:",group_form.errors)  # طباعة الأخطاء
    else:
        group_form = DiaryGroupForm()

    return render(request, 'Group_Diary.html', {'group_form': group_form})

def diary_group_list(request):
    diaries = GroupDiary.objects.all()
    return render(request, 'group_support_diary_list.html', {'diaries': diaries})




from django.contrib import messages
from django.shortcuts import redirect, render
from .models import PersonalRequest, Schedule
from .forms import PersonalRequestForm, ScheduleFormSet

def private_request(request):
    if request.method == 'POST':
        form = PersonalRequestForm(request.POST)
        schedule_formset = ScheduleFormSet(request.POST)

        if form.is_valid() and schedule_formset.is_valid():
            instance = form.save()  # حفظ نموذج الطلب الشخصي
            
            # استخدام schedule_formset.save(commit=False) لتجنب الحفظ المباشر
            schedules = schedule_formset.save(commit=False)
            for schedule in schedules:
                schedule.personal_request = instance  # ربط كل جدول بالنموذج
                schedule.save()  # حفظ كل جدول مرتبط

            messages.success(request, 'הבקשה הוגשה בהצלחה!')
            return redirect('Studentpage')
        else:
            if not schedule_formset.is_valid():
                messages.error(request, 'הנתונים בקובץ השעות אינם תקינים. נא בדוק שוב.')
                print(schedule_formset.errors)  # طباعة الأخطاء للمساعدة في التصحيح
    else:
        form = PersonalRequestForm()
        schedule_formset = ScheduleFormSet()

    return render(request, 'private_request.html', {'form': form, 'schedule_formset': schedule_formset})

from django.shortcuts import render, get_object_or_404
from .models import  PersonalRequest

def manager_view(request):
    students = User.objects.all()  # جلب جميع البيانات من الجدول 'Student'
    return render(request, 'manager_view.html', {'students': students})

def personal_request_detail(request, student_id):
    student = get_object_or_404(User, id=student_id)  # جلب بيانات الطالب حسب معرف الطالب
    requests = PersonalRequest.objects.filter(student=student)  # جلب الطلبات الخاصة بالطالب
    return render(request, 'personal_request_detail.html', {'student': student, 'requests':requests})