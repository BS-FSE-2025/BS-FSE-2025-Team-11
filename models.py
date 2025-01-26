from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from datetime import date


from django.contrib.auth.models import BaseUserManager, AbstractBaseUser , PermissionsMixin, Group, Permission
from django.db import models
from django.core.validators import RegexValidator

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required.')
        if not username:
            raise ValueError('Username is required.')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)

USER_TYPE_CHOICES = [
    ('teacher', 'Teacher'),  # معلم
    ('student', 'Student'),  # طالب
]

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(
        max_length=10,
        unique=True,
        validators=[RegexValidator(r'^\d{10}$', 'The phone number must be exactly 10 digits.')]
    )
    id_number = models.CharField(
        max_length=9,
        unique=True,
        blank=True,null=True,
        validators=[RegexValidator(r'^\d{9}$', 'The ID number must be exactly 9 digits.')]
    )
    specialization = models.CharField(max_length=100)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='student')  # حقل يحدد نوع المستخدم
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def _str_(self):
        return self.username



# models.py

class DeanManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('Username is required.')
        
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)



class Dean(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = DeanManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []  # تحديد الحقول المطلوبة الأخرى عند إنشاء مستخدم جديد، مثل: email, etc.

    def get_success_url(self):
        return reverse('admin_dashboard')

    def _str_(self):
        return self.username


# نموذج رئيسي للمعلومات العامة
class DiaryGroup(models.Model):
    teacher_name = models.CharField(max_length=255, verbose_name="שם המתגבר")
    teacher_id = models.CharField(max_length=50, verbose_name="מספר זהות")
    unit = models.CharField(max_length=255, verbose_name="מחלקה/יחידה", blank=True, null=True)
    course_name = models.CharField(max_length=255, verbose_name="שם הקורס", blank=True, null=True)
    from_date = models.DateField(verbose_name="מתאריך")
    to_date = models.DateField(verbose_name="עד תאריך")
    total_hours = models.PositiveIntegerField(verbose_name="סה''כ שעות לביצוע")
    
    # الحقول الإضافية
    approval_date = models.DateField(verbose_name="תאריך אישור")
    approver_name = models.CharField(max_length=255, verbose_name="שם המאשר")
    position = models.CharField(max_length=255, verbose_name="תפקיד המאשר")
    approved_hours = models.PositiveIntegerField(verbose_name=" סה''כ שעות מאושרות לתשלום")
    signature = models.CharField(max_length=255, verbose_name="חתימה")

    def __str__(self):
        return f"{self.teacher_name} - {self.course_name}"


class DiaryStudent(models.Model):
    group = models.ForeignKey(DiaryGroup, on_delete=models.CASCADE, related_name="students")
    student_name = models.CharField(max_length=255, verbose_name="שם הסטודנט")
    student_date = models.DateField(verbose_name="תאריך נוכחות")
    student_hours = models.PositiveIntegerField(verbose_name="מספר שעות נוכחות")

    def __str__(self):
        return self.student_name



from django.db import models
from django.utils.timezone import now  # لاستيراد التاريخ الحالي

class PrivateDiary(models.Model):
    mentor_name = models.CharField(max_length=100,verbose_name="שם המתגבר")
    id_number = models.CharField(max_length=9,verbose_name="מספר זהות ")
    department = models.CharField(max_length=100 ,verbose_name="התמחות ")
    course_name = models.CharField(max_length=100, verbose_name="שם הקורס")
    start_date = models.DateField(verbose_name="מתאריך")
    end_date = models.DateField(verbose_name="עד תאריך")
    total_hours = models.IntegerField(verbose_name="סה''כ שעות לביצוע")
    approval_date = models.DateField(verbose_name="תאריך אישור", null=True, blank=True)
    approver_name = models.CharField(max_length=255, verbose_name="שם המאשר", null=False, blank=True)
    position = models.CharField(max_length=255, verbose_name="תפקיד המאשר", null=False, blank=True)
    approved_hours = models.PositiveIntegerField(verbose_name=" סה''כ שעות מאושרות לתשלום", null=False, blank=True)
    signature = models.CharField(max_length=255, verbose_name="חתימה", null=False, blank=True)

    def __str__(self):
        return f"{self.mentor_name} - {self.course_name}"


class PrivateSession(models.Model):
    private = models.ForeignKey(PrivateDiary, on_delete=models.CASCADE, related_name="sessions")
    student_date = models.DateField(verbose_name="תאריך", null=True, blank=True, default=now)  # تعيين قيمة افتراضية
    attendance_hours= models.IntegerField(verbose_name="מספר שעות",null=True, blank=True)
    attendance_Topic = models.CharField(max_length=100, verbose_name="נשוא תגבור", null=True, blank=True)
    unit = models.CharField(max_length=100, verbose_name="מחלקה", null=True, blank=True)
    student_name = models.CharField(max_length=255, verbose_name="שם הסטודנט", null=True, blank=True)
    student_signature = models.CharField(max_length=100, verbose_name="חתימת הסטודנט", null=True, blank=True)
    teacher_signature = models.CharField(max_length=100, verbose_name="חתימת המתגבר", null=True, blank=True)

    def __str__(self):
        return f"PrivateSession on {self.student_date}"




class PersonalRequest(models.Model):
    TYPE_CHOICES = [
        ('front', 'תגבור פרונטלי'),
        ('zoom', 'תגבור בזום'),
    ]
    full_name = models.CharField(max_length=100, verbose_name="שם מלא")
    id_number = models.CharField(max_length=9, verbose_name="ת.ז")
    course_name = models.CharField(max_length=255,verbose_name="שם הקורס", blank=True, null=True)
    department = models.CharField(max_length=50, verbose_name="מחלקה")
    year = models.CharField(max_length=4, verbose_name="שנה", blank=True, null=True)
    phone_number = models.CharField(max_length=15, verbose_name="טלפון נייד")
    group_type = models.CharField(max_length=10, choices=TYPE_CHOICES, blank=True, null=True)
    email = models.EmailField(verbose_name="כתובת מייל")
    mentor_name = models.CharField(max_length=100,verbose_name="שם המתגבר", blank=True, null=True)
    status=models.CharField( max_length=20,blank=True,null=True,default='Panding')
    def __str__(self):
        return f"{self.full_name} ({self.id_number})"


class Schedule(models.Model):
    private = models.ForeignKey(PersonalRequest, on_delete=models.CASCADE, related_name="Schedules")  # هنا 1 هو ID لطلب شخصي موجود
    student_day = models.CharField(max_length=255, verbose_name="יום",null=True, blank=True)
    start_time = models.CharField(max_length=255, verbose_name="משעה", null=True, blank=True)
    end_time = models.CharField(max_length=255, verbose_name="עד שעה", null=True, blank=True)

    def __str__(self):
        return f"PersonalRequest on {self.student_day}"



from django.db import models

class GroupRequest(models.Model):
    COURSE_TYPE_CHOICES = [
        ('front', 'תגבור פרונטלי'),
        ('zoom', 'תגבור בזום'),
    ]


    course_name = models.CharField(max_length=255, verbose_name="שם הקורס")
    course_number = models.PositiveIntegerField(verbose_name="מספר הקורס")
    department = models.CharField(max_length=255, verbose_name="מחלקה")
    campus = models.CharField(max_length=255,verbose_name="קמפוס")
    group_type = models.CharField(max_length=10, choices=COURSE_TYPE_CHOICES,verbose_name="סוג הקבוצה")
    mentor_name = models.CharField(max_length=100,verbose_name="שם המתגבר", blank=True, null=True)
    contact_name = models.CharField(max_length=255, verbose_name="שם איש הקשר")
    contact_id = models.CharField(max_length=9, verbose_name="תעודת זהות של איש הקשר")
    contact_department = models.CharField(max_length=255, verbose_name="מחלקת איש הקשר")
    contact_campus = models.CharField(max_length=255, verbose_name="קמפוס של איש הקשר")
    contact_phone = models.CharField(max_length=15, verbose_name="טלפון של איש הקשר")
    contact_email = models.EmailField(verbose_name="אימייל של איש הקשר")
    status=models.CharField( max_length=20,blank=True,null=True,default='Panding')

    def __str__(self):
        return f"{self.course_name} - {self.contact_name}"


class GroupOption(models.Model):
    group_request = models.ForeignKey(GroupRequest, on_delete=models.CASCADE, related_name='session_options')
    day = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()


class GroupStudents(models.Model):
    group_request = models.ForeignKey(GroupRequest, on_delete=models.CASCADE, related_name='students')
    student_name = models.CharField(max_length=255)
    signature = models.CharField(max_length=255, blank=True)
    student_department = models.CharField(max_length=255)

    def __str__(self):
        return self.student_name
