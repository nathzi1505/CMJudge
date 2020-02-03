from django.urls import path

from . import views

urlpatterns = [
    path("register", views.register, name="register"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("course_enrollment", views.add_student_to_course, name="course_enrollment"),
    path("submissions", views.get_submissions, name="submissions"),
    path("", views.index, name="index"),
    path("<str:abbreviation>", views.course, name="course"),
    path("<str:abbreviation>/<str:as_code>", views.assignment, name="assignment"),
    path("<str:abbreviation>/<str:as_code>/<str:code>", views.question, name="question"),
    path("<str:abbreviation>/<str:as_code>/<str:code>/submit", views.submit, name="submit"),
    path("<str:abbreviation>/<str:as_code>/<str:code>/results", views.results, name="results"),
]