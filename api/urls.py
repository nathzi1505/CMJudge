from django.urls import path

from . import views

urlpatterns = [
    path("register", views.register, name="register"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("submissions", views.get_submissions, name="submissions"),
    path("", views.index, name="index"),
    path("<str:abbreviation>", views.course, name="course"),
    path("<str:abbreviation>/<str:as_code>", views.assignment, name="assignment"),
    path("<str:abbreviation>/<str:as_code>/<str:code>", views.question, name="question"),
    path("<str:abbreviation>/<str:as_code>/<str:code>/submit", views.submit, name="submit"),
    path("<str:abbreviation>/<str:as_code>/<str:code>/submit/text", views.submit_text, name="submit_text"),
]