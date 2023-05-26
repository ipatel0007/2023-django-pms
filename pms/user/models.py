from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    is_euser = models.BooleanField(default=False)
    is_advisor = models.BooleanField(default=False)
    address = models.CharField(max_length=100)
    annual_income = models.IntegerField(default=0)
    phone_no = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'user'



