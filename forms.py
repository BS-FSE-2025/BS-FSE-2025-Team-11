# forms.py
from django import forms
from django.core.exceptions import ValidationError
from .models import User  
from django.forms import formset_factory
from .models import DiaryGroup, DiaryStudent

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

from .models import PersonalRequest, Schedule
from django.forms.models import inlineformset_factory

class PersonalRequestForm(forms.ModelForm):
    class Meta:
        model = PersonalRequest
        fields = ['full_name', 'id_number', 'department', 'year', 'phone_number', 'email']



class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['day', 'time']

    def save(self, commit=True):
        schedule = super().save(commit=False)
        schedule.day = self.cleaned_data.get('day')
        schedule.time = self.cleaned_data.get('time')
        
        if commit:
            schedule.save()
        return schedule

ScheduleFormSet = inlineformset_factory(
    PersonalRequest,
    Schedule,
    fields=['day', 'time'],
    extra=1
)