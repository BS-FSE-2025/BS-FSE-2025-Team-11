from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=255)  # يجب تخزين كلمة المرور مشفرة
    email = models.EmailField()
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    id_number = models.CharField(max_length=20, blank=True, null=True)
    specialization = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
