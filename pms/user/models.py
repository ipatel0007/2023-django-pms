from django.db import models
from django.contrib.auth.models import AbstractUser








class User(AbstractUser):
    is_euser = models.BooleanField(default=False)
    is_advisor = models.BooleanField(default=False)
    address = models.CharField(max_length=100)
    annual_income = models.IntegerField(default=0)
    phone_no = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'user'
        
class EnrollmentRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    advisor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='advisor')
    status_choices = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected')
    )
    status = models.CharField(choices=status_choices, default='PENDING', max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'enrollment_request'

    def __str__(self):
        return self.status


