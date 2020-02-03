from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from teacher.models import *

# Create your models here.
class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    code = models.CharField(max_length=10, unique=True, validators=[RegexValidator('^[A-Z_]*$',
                               'Only uppercase letters and underscores allowed.')])
    name = models.CharField(max_length=64, validators=[RegexValidator('^[A-Z_]*$',
                              'Only uppercase letters and underscores allowed.')])
    
    def __str__(self):
        return (f"Assignment : {self.name}")

class Question(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    code = models.CharField(max_length=10, unique=True, validators=[RegexValidator('^[A-Z_]*$',
                               'Only uppercase letters and underscores allowed.')])
    name = models.CharField(max_length=64)
    problem_desc = models.TextField()
    sample_input = models.TextField()
    sample_output = models.TextField()
    discussions = models.TextField(default=None, null=True, blank=True)
    difficulty = models.PositiveIntegerField(default=1,
        validators=[MaxValueValidator(5), MinValueValidator(1)])

    def __str__(self):
        return (f"{self.assignment.name}, Name : {self.name}")

class TestCase(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    description = models.CharField(max_length=32, null=True)
    input_case = models.TextField()
    output_case = models.TextField()
    
    def __str__(self):
        return (f"{self.question.assignment.course.name}, {self.question.assignment.name}, {self.question.name}, \
        Description : {self.description}")
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_no = models.CharField(max_length=12, validators=[RegexValidator('^[0-9]*$',
                               'Only digits allowed.')], unique=True)
    course = models.ManyToManyField(Course)
    
    def __str__(self):
        return (f"Name : {self.user.get_full_name()}, Roll No : {self.roll_no}")

class Submission(models.Model):
    student = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    time_of_submission = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return (f"Name : {self.student.user.get_full_name()}, Roll No : {self.student.roll_no}, \
                Question : {self.question.name}, Assignment : {self.question.assignment.name}, \
                Course : {self.question.assignment.course.name}, Time : {self.time_of_submission}")

    