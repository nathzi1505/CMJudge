from django.urls import path

from . import views
from . import api
from . import csv

urlpatterns = [
    
    path("api/course/register", api.course_register, name="api_course_register"),
    path("api/register", api.register, name="api_register"),
    path("api/login", api.login, name="api_login"),
    path("api/superuser_login", api.superuser_login, name="api_superuser_login"),
    path("api/course_enrollment", api.add_student_to_course, name="course_enrollment"),
    path("api/<str:abbreviation>", api.course, name="course"),
    path("api/<str:abbreviation>/set", api.set_assignment, name="set_assignment"),
    path("api/<str:abbreviation>/<str:code>", api.assignment, name="assignment"),
    path("api/<str:abbreviation>/<str:code>/set", api.set_question, name="set_question"),
    path("api/<str:abbreviation>/<str:as_code>/<str:code>", api.question, name="question"),
    path("api/<str:abbreviation>/<str:as_code>/<str:code>/testcase", api.add_testcase, name="add_testcase"),
    path("api/", api.index, name="api_index"),
    
    path("csv/<str:abbreviation>/<str:as_code>", csv.get_assignment_csv, name="assignment_csv"),
    path("csv/<str:abbreviation>/<str:as_code>/<str:code>", csv.get_question_csv, name="question_csv"),
    
    path("register", views.register, name="register"),
    path("login", views.login, name="login"),
    path("superuser_login", views.superuser_login, name="superuser_login"),
    path("course/register", views.course_register, name="course_register"),
    path("", views.index, name="index"),
    path("<str:abbreviation>", views.course, name="course"),
    path("<str:abbreviation>/set", views.set_assignment, name="set_assignment"),
    path("<str:abbreviation>/<str:code>", views.assignment, name="assignment"),
    path("<str:abbreviation>/<str:code>/set", views.set_question, name="set_question"),
    path("<str:abbreviation>/<str:as_code>/<str:code>", views.question, name="question"),
    path("<str:abbreviation>/<str:as_code>/<str:code>/testcase", views.add_testcase, name="add_testcase"),
    
]