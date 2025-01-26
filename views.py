from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse
from django.shortcuts import  get_object_or_404
from django.forms import modelformset_factory
from .forms import PersonalRequestForm,ScheduleForm
from .models import Schedule,PersonalRequest
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required

def contact_Dean(request):
    return render(request, 'contactStudent.html')
def contd_view(request):
    return render(request, 'ContD.html')
def contactd_view(request):
    return render(request, 'contactStudent.html')
def contd_view(request):
    return render(request, 'ContD.html')
def home(request):
    return render(request, 'home.html')
def najah(request):
    return render(request, 'najah.html')

def Teacherpage(request):
    porsonals= PrivateDiary.objects.all()
    groups = DiaryGroup.objects.all()
    context = {
        'porsonals': porsonals,
        'groups': groups,
    }
    return render(request, 'Teacherpage.html')

def Studentpage(request):
    group_requests = GroupRequest.objects.all() 
    privates = PersonalRequest.objects.all()
    context = {
        'group_requests': group_requests,
        'privates': privates,
    }
    return render(request, 'Studentpage.html', context)
def Group_Diary(request):
    return render(request, 'Group_Diary.html')
def private_Diary(request):
    return render(request, 'private_Diary.html')

def Update_time(request):
    return render(request, 'Update_time.html') 
def dean_page(request):
    return render(request, 'dean_page.html') 

def first_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')
        id_number = request.POST.get('id_number')
        specialization = request.POST.get('specialization')


        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please log in.')
            return redirect('login_M')


        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists. Please log in.')
            return redirect('login_M')

        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password),
            phone_number=phone_number,
            id_number=id_number,
            specialization=specialization,
            user_type='teacher',  
        )

        login(request, user)
        messages.success(request, 'Account successfully created.')
        return redirect('Teacherpage')

    return render(request, 'first_login.html')


# Login function

def login_M(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        print(f"Username entered: {username}")
        print(f"Password entered: {password}")

        try:
            user = User.objects.get(username=username)
            print(f"User found: {user}")
        except User.DoesNotExist:
            print("User does not exist")
            messages.error(request, 'Invalid username or password.')
            return render(request, 'login_M.html')

        # التحقق من كلمة المرور
        if user.check_password(password):
            if user.is_active and user.user_type == 'teacher':
                login(request, user)
                messages.success(request, f'Welcome, {user.username}!')
                return redirect('Teacherpage')
            else:
                print("User is not active or not a student.")
                messages.error(request, 'You are not an active student.')
        else:
            print("Password is incorrect.")
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login_M.html')

def Signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')
        id_number = request.POST.get('id_number')
        specialization = request.POST.get('specialization')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please log in.')
            return redirect('login_S')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists. Please log in.')
            return redirect('login_S')

        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password),
            phone_number=phone_number,
            id_number=id_number,
            specialization=specialization,
            user_type='student',  # تحديد النوع كطالب
            is_active=True,
        )

        login(request, user)
        messages.success(request, 'Account successfully created.')
        return redirect('Studentpage')

    return render(request, 'Sign_up.html')


# Login function
def login_S(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        print(f"Username entered: {username}")
        print(f"Password entered: {password}")

        try:
            user = User.objects.get(username=username)
            print(f"User found: {user}")
        except User.DoesNotExist:
            print("User does not exist")
            messages.error(request, 'Invalid username or password.')
            return render(request, 'login_S.html')

        # التحقق من كلمة المرور
        if user.check_password(password):
            if user.is_active and user.user_type == 'student':
                login(request, user)
                messages.success(request, f'Welcome, {user.username}!')
                return redirect('Studentpage')
            else:
                print("User is not active or not a student.")
                messages.error(request, 'You are not an active student.')
        else:
            print("Password is incorrect.")
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login_S.html')

# عرض جميع المستخدمين (اختبار)
def test_view(request):
    records = User.objects.all()  # استرداد جميع السجلات
    return render(request, 'test_view.html', {'records': records})

def authenticate_dean(username, password):
    # بيانات المستخدمين المسموح لهم بالدخول
    allowed_users = {
        'doha': 'doha1',
        'shaima': 'shaima11',
        'marwa': 'marwa1',
        'tmara': 'tmara1',

    }

    # تحقق من أن اسم المستخدم وكلمة المرور صحيحة
    if username in allowed_users and allowed_users[username] == password:
        return username
    return None

def Deanlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # محاولة المصادقة
        dean = authenticate_dean(username, password)
        if dean is not None:
            messages.success(request, f'Welcome')
            return redirect('dean_page')  # تأكد من أنك قد قمت بإضافة هذا الرابط في urls.py
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('Deanlogin')

    return render(request, 'Deanlogin.html')


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
            student_names = request.POST.getlist('student_name[]')
            attendance_dates = request.POST.getlist('student_date[]')
            attendance_hours_list = request.POST.getlist('student_hours[]')

            # استخدام الحد الأقصى لطول القائمة لتجنب التوقف عند الطول الأقل
            max_length = max(len(student_names), len(attendance_dates), len(attendance_hours_list))

            for i in range(max_length):
                # الحصول على القيم مع معالجة حالة عدم وجودها
                student_name = student_names[i] if i < len(student_names) else None
                student_date = attendance_dates[i] if i < len(attendance_dates) else None
                student_hours = attendance_hours_list[i] if i < len(attendance_hours_list) else None
                
                # التحقق من أن جميع القيم صالحة قبل إضافتها
                if student_name and student_date and student_hours:
                    try:
                        students.append(DiaryStudent(
                            group=group,
                            student_name=student_name,
                            student_date=student_date,
                            student_hours=int(student_hours)  # تحويل الساعات إلى عدد صحيح
                        ))
                    except Exception as e:
                        print(f"Error adding student data: {e}")
            
            # إنشاء السجلات دفعة واحدة إذا كانت هناك بيانات
            if students:
                try:
                    DiaryStudent.objects.bulk_create(students)
                except Exception as e:
                    print(f"Error saving students: {e}")

            return redirect('Najah')
        else:
            print("Form errors:", group_form.errors)  # طباعة أخطاء النموذج
    else:
        group_form = DiaryGroupForm()

    return render(request, 'Group_Diary.html', {'group_form': group_form})




from .forms import PrivateDiaryForm, SessionForm
from .models import PrivateDiary, PrivateSession
from datetime import datetime


def private_Diary(request):
    if request.method == 'POST':
        private_form = PrivateDiaryForm(request.POST)
        if private_form.is_valid():
            private = private_form.save()
            sessions = []

            # الحصول على البيانات من الطلب
            student_dates = request.POST.getlist('student_date[]')
            attendance_hours_list = request.POST.getlist('attendance_hours[]')
            attendance_topics = request.POST.getlist('attendance_Topic[]')
            units = request.POST.getlist('unit[]')
            student_names = request.POST.getlist('student_name[]')
            student_signatures = request.POST.getlist('student_signature[]')
            teacher_signatures = request.POST.getlist('teacher_signature[]')

            # معالجة الأطوال غير المتساوية
            max_length = max(len(student_dates), len(attendance_hours_list), len(attendance_topics),
                             len(units), len(student_names), len(student_signatures), len(teacher_signatures))

            for i in range(max_length):
                student_date = student_dates[i] if i < len(student_dates) else None
                attendance_hours = attendance_hours_list[i] if i < len(attendance_hours_list) else None
                attendance_Topic = attendance_topics[i] if i < len(attendance_topics) else None
                unit = units[i] if i < len(units) else None
                student_name = student_names[i] if i < len(student_names) else None
                student_signature = student_signatures[i] if i < len(student_signatures) else None
                teacher_signature = teacher_signatures[i] if i < len(teacher_signatures) else None

                # تحقق من أن كل الحقول مطلوبة
                if student_date and attendance_hours and attendance_Topic and unit and student_name and student_signature and teacher_signature:
                    sessions.append(PrivateSession(
                        private=private,
                        student_date=student_date,
                        attendance_hours=attendance_hours,
                        attendance_Topic=attendance_Topic,
                        unit=unit,
                        student_name=student_name,
                        student_signature=student_signature,
                        teacher_signature=teacher_signature,
                    ))

            # إنشاء الجلسات دفعة واحدة
            if sessions:
                PrivateSession.objects.bulk_create(sessions)

            return redirect('Najah')
        else:
            print("Form errors:", private_form.errors)
    else:
        private_form = PrivateDiaryForm()

    return render(request, 'private_Diary.html', {'private_form': private_form})
from django.contrib.auth import logout
from django.shortcuts import redirect
@login_required
def logout(request):
    logout(request)
    return redirect('home')  # הפנייה לעמוד הבית אחרי ה-logout

def private_request(request):
    if request.method == 'POST':
        private_form = PersonalRequestForm(request.POST)
        if private_form.is_valid():
            private = private_form.save()  # حفظ النموذج الأساسي
            schedules = []
            student_days = request.POST.getlist('student_day[]')
            start_times = request.POST.getlist('start_time[]')
            end_times = request.POST.getlist('end_time[]')

            # التأكد من أن طول القوائم متساوي
            max_length = max(len(student_days), len(start_times),len(end_times))
            for i in range(max_length):
                student_day = student_days[i] if i < len(student_days) else None
                start_time = start_times[i] if i < len(start_times) else None
                end_time = end_times[i] if i < len(end_times) else None
                # التأكد من أن الحقول غير فارغة
                if student_day and end_time and start_time:
                    schedules.append(Schedule(
                        private=private,  # ربط السجل مع الطلب الشخصي
                        student_day=student_day,
                        start_time=start_time,end_time=end_time
                    ))

            # إذا كانت هناك مواعيد، يتم إنشاء الجداول باستخدام bulk_create
            if schedules:
                Schedule.objects.bulk_create(schedules)

            return redirect('Najah')
        else:
            print("Form errors:", private_form.errors)
    else:
        private_form = PersonalRequestForm()

    return render(request, 'private_request.html', {'private_form': private_form})





from .models import GroupRequest
from django.shortcuts import render, redirect
from .forms import GroupRequestForm, GroupOptionForm, GroupStudentsForm
from django.forms import formset_factory

def Group_request(request):
    GroupOptionFormSet = formset_factory(GroupOptionForm, extra=1)
    GroupStudentsFormSet = formset_factory(GroupStudentsForm, extra=1)

    if request.method == 'POST':
        
        group_form = GroupRequestForm(request.POST)
        session_formset = GroupOptionFormSet(request.POST, prefix='sessions')
        student_formset = GroupStudentsFormSet(request.POST, prefix='students')

        if group_form.is_valid() and session_formset.is_valid() and student_formset.is_valid():
            group_request = group_form.save()

            for session_form in session_formset:
                if session_form.cleaned_data:
                    session = session_form.save(commit=False)
                    session.group_request = group_request
                    session.save()

            for student_form in student_formset:
                if student_form.cleaned_data:
                    student = student_form.save(commit=False)
                    student.group_request = group_request
                    student.save()

            return redirect('Najah')  # استبدل بـ URL النجاح الخاص بك

    else:
        group_form = GroupRequestForm()
        session_formset = GroupOptionFormSet(prefix='sessions')
        student_formset = GroupStudentsFormSet(prefix='students')

    return render(request, 'Group_request.html', {
        'group_form': group_form,
        'session_formset': session_formset,
        'student_formset': student_formset,
    })




from django.shortcuts import render, get_object_or_404, redirect
from .models import GroupRequest, PersonalRequest 
from django.shortcuts import render, get_object_or_404, redirect
from .models import GroupRequest, PersonalRequest  # تأكد من استيراد النموذجين

def delete_group_request_view(request, request_id):
    # جلب الطلب بناءً على الـ ID
    group_request = get_object_or_404(GroupRequest, id=request_id)

    if request.method == 'POST':
        # حذف الطلب
        group_request.delete()
        return redirect('Studentpage')  # إعادة التوجيه إلى صفحة Studentpage

    # عرض صفحة التأكيد
    return render(request, 'delete_group_request.html', {'group_request': group_request})


def delete_private_request_view(request, request_id):
    # جلب الطلب بناءً على الـ ID
    private = get_object_or_404(PersonalRequest, id=request_id)

    if request.method == 'POST':
        # حذف الطلب
        private.delete()
        return redirect('Studentpage')  # إعادة التوجيه إلى صفحة Studentpage

    # عرض صفحة التأكيد
    return render(request, 'delete_private_request.html', {'private': private})

    # عرض صفحة تأكيد الحذف
    return render(request, 'delete_private_diary.html', {'private_diary': private_diary})




from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import PersonalRequest


@csrf_exempt
def dean_requests_view(request):
    if request.method == "POST":
        request_id = request.POST.get("request_id")
        action = request.POST.get("action")
        
        # استخدام filter بدلاً من get
        personal_requests = PersonalRequest.objects.filter(id_number=request_id)
        group_requests = GroupRequest.objects.filter(contact_id=request_id)

        if group_requests.exists():
            # تحديث الحالة لجميع السجلات المطابقة
            for group_request in group_requests:
                if action == "approve":
                    group_request.status = "מַאֲשָׁר"  # موافقة
                elif action == "reject":
                    group_request.status = "דָּחָה"  # رفض
                group_request.save()  # حفظ التغييرات في قاعدة البيانات
        else:
            print("לא נמצא בקשה עם מספר זהות זה")  # إذا لم يتم العثور على الطلب
        
        if personal_requests.exists():
            # تحديث الحالة لجميع السجلات المطابقة
            for personal_request in personal_requests:
                if action == "approve":
                    personal_request.status = "מַאֲשָׁר"  # موافقة
                elif action == "reject":
                    personal_request.status = "דָּחָה"  # رفض
                personal_request.save()  # حفظ التغييرات في قاعدة البيانات
        else:
            print("לא נמצא בקשה עם מספר זהות זה")  # إذا لم يتم العثور على الطلب

        return redirect("dean_requests")  # إعادة تحميل الصفحة

    # جمع البيانات لتمريرها إلى القالب
    requests = PersonalRequest.objects.all()
    groups = GroupRequest.objects.all()
    context = {
        "requests": requests,
        "groups": groups
    }
    return render(request, "dean_requests.html", context)



from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

def request_status_view(request):
    status = None
    full_name = None

    if request.method == "POST":
        # استلام اسم المستخدم المدخل
        entered_name = request.POST.get('id_number')
        
        # البحث عن الطلب باستخدام اسم المستخدم
        try:
            student_request = PersonalRequest.objects.get(id_number=entered_name)
            status = student_request.status
            id_number = student_request.id_number
        except PersonalRequest.DoesNotExist:
            return HttpResponse("לא נמצא משתמש עם שם זה", status=404)  # رسالة الخطأ إذا لم يتم العثور على اسم المستخدم

    return render(request, 'request_status.html', {'status': status, 'id_number': id_number})

def manage_users(request):
    users = User.objects.all()
    return render(request, 'manage_users.html', {'users': users})    


def system_Teacher_view(request):
    personal_requests = PersonalRequest.objects.prefetch_related('Schedules')
    group_requests = GroupRequest.objects.prefetch_related('session_options','students')

    context = {
        'personal_requests': personal_requests,
        'group_requests': group_requests,
    }
    return render(request, 'system_Teacher.html', context)

def update_user(request, user_id):
    if request.method == 'POST':
        # الحصول على المستخدم من قاعدة البيانات
        user = get_object_or_404(User, id=user_id)
        # تحديث الحقول بناءً على المدخلات
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.phone_number = request.POST.get('phone_number')
        user.id_number = request.POST.get('id_number')
        user.specialization = request.POST.get('specialization')
        # حفظ التغييرات
        user.save()
        return redirect('manage_users')  # إعادة التوجيه إلى صفحة إدارة المستخدمين
    else:
        return HttpResponseForbidden("אסור")


def system_Student_view(request):

    personal_requests = PersonalRequest.objects.prefetch_related('Schedules')
    group_requests = GroupRequest.objects.prefetch_related('session_options','students')

    context = {
        'personal_requests': personal_requests,
        'group_requests': group_requests,
    }
    return render(request, 'system_Student.html', context)

# تحديث الساعات في الطلبات الشخصية
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden

# تحديث الساعات في الطلبات الشخصية
def update_time(request, requset_id):
    if request.method == 'POST':
        # الحصول على الطلب الشخصي باستخدام ID
        user = get_object_or_404(PersonalRequest, id=requset_id)
        
        # تحديث البيانات الشخصية
        user.full_name = request.POST.get('full_name')
        user.id_number = request.POST.get('id_number')
        user.course_name = request.POST.get('course_name')
        user.student_day = request.POST.get('student_day')

        # تحديث الوقت (الساعات)
        schedule = user.Schedules.first()  # الحصول على أول جدول (إذا وجد)
        if schedule:
            schedule.start_time = request.POST.get('start_time')
            schedule.end_time = request.POST.get('end_time')
            schedule.save()

        user.save()
        
        # بدلاً من إعادة التوجيه إلى صفحة أخرى، نقوم بإعادة تحميل نفس الصفحة
        # تحميل نفس الصفحة (system_Teacher) مع البيانات المعدلة
        personal_requests = PersonalRequest.objects.prefetch_related('Schedules')
        group_requests = GroupRequest.objects.prefetch_related('session_options', 'students')
        context = {
            'personal_requests': personal_requests,
            'group_requests': group_requests,
        }
        return render(request, 'system_Teacher.html', context)
    else:
        return HttpResponseForbidden("אסור")  # إذا كانت الطريقة غير صحيحة


# تحديث الساعات في الطلبات الجماعية
def update_timeG(request, group_id):
    if request.method == 'POST':
        # الحصول على طلب المجموعة باستخدام ID
        group = get_object_or_404(GroupRequest, id=group_id)
        
        # تحديث البيانات الخاصة بالمجموعة
        group.contact_name = request.POST.get('contact_name')
        group.contact_id = request.POST.get('contact_id')
        group.course_name = request.POST.get('course_name')
        group.day = request.POST.get('day')

        # تحديث وقت الجلسة في المجموعة
        groupOption = group.session_options.first()  # الحصول على أول خيار مجموعة
        if groupOption:
            groupOption.start_time = request.POST.get('start_time')
            groupOption.end_time = request.POST.get('end_time')
            groupOption.save()
        else:
            return HttpResponseForbidden("אסור")  # إذا لم توجد خيارات للمجموعة، يرجى إرجاع استجابة ممنوعة

        group.save()

        # بدلاً من إعادة التوجيه إلى صفحة أخرى، نقوم بإعادة تحميل نفس الصفحة
        group_requests = GroupRequest.objects.prefetch_related('session_options', 'students')
        personal_requests = PersonalRequest.objects.prefetch_related('Schedules')
        context = {
            'personal_requests': personal_requests,
            'group_requests': group_requests,
        }
        return render(request, 'system_Teacher.html', context)
    else:
        return HttpResponseForbidden("אסור")  # إذا كانت الطريقة غير صحيحة

        





#מחק סטודנט
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('manage_users')







from django.shortcuts import render
from .models import PrivateDiary, PrivateSession

def admin_dashboard(request):
    # جلب جميع بيانات PrivateDiary

    diaries = PrivateDiary.objects.all()
    groups=DiaryGroup.objects.all()
    # جلب جميع بيانات PrivateSession (لزر יומן פרטי)
    sessions = PrivateSession.objects.all()
    students = DiaryStudent.objects.all()
    return render(request, 'admin_dashboard.html', {
        'diaries': diaries,
        'sessions': sessions,
        'groups':groups,
        'students': students,

    })


from django.shortcuts import render, get_object_or_404
from .models import PrivateDiary

def private_diary_view(request, diary_id):
    # استرجاع اليومية بناءً على الـ id
    diary = get_object_or_404(PrivateDiary, id=diary_id)

    # استرجاع الجلسات المرتبطة باستخدام related_name
    sessions = diary.sessions.all()

    # إرسال البيانات إلى القالب
    return render(request, 'private_diary_view.html', {
        'diary': diary,
        'sessions': sessions,
    })

def group_diary_view(request, group_id):
    # استرجاع مجموعة اليوميات بناءً على المعرف
    group = get_object_or_404(DiaryGroup, id=group_id)
    
    # استرجاع جميع الطلاب المتعلقين بالمجموعة
    students = group.students.all()

    return render(request, 'group_diary_view.html', {
        'group': group,
        'students': students,
    })