
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from datetime import date


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
        validators=[RegexValidator(r'^\d{9}$', 'The ID number must be exactly 9 digits.')]
    )
    specialization = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)


    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def _str_(self):
        return self.username

# models.py


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
    approved_hours = models.PositiveIntegerField(verbose_name="סה''כ שעות מאושרות")
    signature = models.CharField(max_length=255, verbose_name="חתימה")

    def _str_(self):
        return f"{self.teacher_name} - {self.course_name}"


class DiaryStudent(models.Model):
    group = models.ForeignKey(DiaryGroup, on_delete=models.CASCADE, related_name="students")
    student_name = models.CharField(max_length=255, verbose_name="שם הסטודנט")
    attendance_date = models.DateField(verbose_name="תאריך נוכחות")
    attendance_hours = models.PositiveIntegerField(verbose_name="מספר שעות נוכחות")

    def _str_(self):
        return self.student_name




class PersonalRequest(models.Model):
    full_name = models.CharField(max_length=100, verbose_name="שם מלא")
    id_number = models.CharField(max_length=9, verbose_name="ת.ז", unique=True)
    department = models.CharField(max_length=50, verbose_name="מחלקה")
    year = models.CharField(max_length=4, verbose_name="שנה",blank=True,null=True)
    phone_number = models.CharField(max_length=15, verbose_name="טלפון נייד")
    email = models.EmailField(verbose_name="כתובת מייל")

    def str(self):
        return f"{self.full_name} ({self.id_number})"

class Schedule(models.Model):
    personal_Request = models.ForeignKey(
        'PersonalRequest', 
        on_delete=models.CASCADE,
        related_name="schedules",
    )
    day = models.CharField(max_length=20, verbose_name="יום",blank=True,null=True)
    time = models.TimeField(blank=True,null=True)

    def str(self):
        return f"{self.day} - {self.time} ({self.personal_Request.full_name})"

