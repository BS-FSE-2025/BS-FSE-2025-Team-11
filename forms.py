# forms.py
from django import forms
from django.core.exceptions import ValidationError
from .models import User, Dean 
from django.forms import formset_factory
from .models import DiaryGroup, DiaryStudent
from datetime import datetime

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=8, required=True)
    
    class Meta:
        model = User  # استخدام نموذج المستخدم المخصص الخاص بك
        fields = ['username', 'email', 'password', 'phone_number', 'id_number', 'specialization']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists.")
        return email

# forms.py
class DeanForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=8, required=True)
    
    class Meta:
        model = Dean  # استخدام نموذج المستخدم المخصص الخاص بك
        fields = ['username','password']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already exists.")
        return username
    




class DiaryGroupForm(forms.ModelForm):
    class Meta:
        model = DiaryGroup
        fields = [
            'teacher_name', 'teacher_id', 'unit', 'course_name', 'from_date', 
            'to_date', 'total_hours', 'approval_date', 'approver_name', 
            'position', 'approved_hours', 'signature',
        ]
        widgets = {
            'from_date': forms.DateInput(attrs={'type': 'date'}),
            'to_date': forms.DateInput(attrs={'type': 'date'}),
            'approval_date': forms.DateInput(attrs={'type': 'date'}),
        }





from .models import PersonalRequest, Schedule
from django.forms.models import inlineformset_factory

class PersonalRequestForm(forms.ModelForm):
    class Meta:
        model = PersonalRequest
        fields = ['full_name', 'id_number', 'department', 'year', 'phone_number', 'email','course_name',
        'mentor_name','group_type']
       




class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['student_day', 'start_time','end_time']

    def save(self, commit=True):
        schedule = super().save(commit=False)
        if commit:
            schedule.save()
        return schedule


ScheduleFormSet = inlineformset_factory(
    PersonalRequest,
    Schedule,
    fields=['student_day',  'start_time','end_time'],
    extra=1
)


from django import forms
from .models import PrivateDiary, PrivateSession

class PrivateDiaryForm(forms.ModelForm):
    class Meta:
        model = PrivateDiary
        fields = [
            'mentor_name',
            'id_number',
            'department',
            'course_name',
            'start_date',
            'end_date',
            'total_hours','approver_name','position','approved_hours','approval_date','signature'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }



class SessionForm(forms.ModelForm):
    class Meta:
        model = PrivateSession
        fields = [
            'student_date',
            'attendance_hours',
            'attendance_Topic',
            'unit',
            'student_name',
            'student_signature',
            'teacher_signature',
        ]
        def clean_student_date(self):
            input_date = self.cleaned_data['student_date']
            try:
              # افترض أن المستخدم يدخل التاريخ بتنسيق DD/MM/YYYY
                parsed_date = datetime.strptime(input_date, "%d/%m/%Y").date()
                return parsed_date
            except ValueError:
                raise forms.ValidationError("Invalid date format. Please use DD/MM/YYYY.")



from django import forms
from .models import GroupRequest, GroupOption, GroupStudents

class GroupRequestForm(forms.ModelForm):
    class Meta:
        model = GroupRequest
        fields = [
            'course_name', 'course_number', 'department', 'campus', 'group_type',
            'contact_name', 'contact_id', 'contact_department', 'contact_campus',
            'contact_phone', 'contact_email','mentor_name'
        ]


class GroupOptionForm(forms.ModelForm):
    class Meta:
        model = GroupOption
        fields = ['day', 'start_time', 'end_time']
        widgets = {
            'day': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.DateInput(attrs={'type': 'time'}),
            'end_time': forms.DateInput(attrs={'type': 'time'}),
        }


class GroupStudentsForm(forms.ModelForm):
    class Meta:
        model = GroupStudents
        fields = ['student_name', 'signature', 'student_department']

