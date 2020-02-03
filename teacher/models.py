from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return (f"Prof. {self.user.get_full_name()}")

class Course(models.Model):
    name = models.CharField(max_length=32, unique=True)
    abbreviation = models.CharField(max_length=10, unique=True)
    code = models.CharField(max_length=32, unique=True)
    teacher = models.ManyToManyField(Teacher)
    
    def __str__(self):
        return (f"Code : {self.code}, Name : {self.name}")