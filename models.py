
from django.db import models

class Request(models.Model):
    subject = models.CharField(max_length=100)  # اسم المادة
    status = models.CharField(
        max_length=50,
        choices=[
            ('Pending', 'בהמתנה'),
            ('Approved', 'מאושר'),
            ('Rejected', 'נדחתה'),
        ]
    )  
    created_at = models.DateTimeField(auto_now_add=True)  # وقت إنشاء الطلب

    def __str__(self):
        return f"{self.subject} - {self.status}"
