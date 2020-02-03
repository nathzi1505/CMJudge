from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from api.tasks import *
from api.exceptions import *
from . tasks import *
from . models import *


@teacher_login_required_html
def index(request):
    if request.method == "GET":
        teacher_username = request.session['user']['username']
        teacher = User.objects.get(username=teacher_username).teacher
        context = {
            "courses": Course.objects.filter(teacher=teacher),
        }
        return render(request, "teacher/index.html", context)
    else:
        raise Http404

@teacher_login_required_html
def set_assignment(request, abbreviation):
    if request.method == "GET":
        course = Course.objects.get(abbreviation=abbreviation)
        if course is not None:
            course = {
                "name" : course.name,
                "abbreviation" : course.abbreviation,
                "code": course.code,
            }
            context = {
                "course": course,
            }
            return render(request, "teacher/set_assignment.html", context)
        else:
            raise Http404

@teacher_login_required_html
def set_question(request, abbreviation, code):
    if request.method == "GET":
        course = Course.objects.get(abbreviation=abbreviation)
        assignment = Assignment.objects.get(course=course, code=code)
        if (course is not None and assignment is not None):
            course = {
                "name" : course.name,
                "abbreviation" : course.abbreviation,
                "code": course.code,
            }
            assignment = {
                "name" : assignment.name,
                "code" : assignment.code,
            }
            context = {
                "course": course,
                "assignment": assignment,
            }
            return render(request, "teacher/set_question.html", context)
        else:
            raise Http404

@teacher_login_required_html
def course(request, abbreviation):
    if request.method == "GET":
        course = Course.objects.get(abbreviation=abbreviation)
        assignments = Assignment.objects.filter(course=course)
        
        if len(assignments) == 0:
            raise Http404
        context = {
            "course": course,
            "assignments": assignments,
        }
        return render(request, "teacher/course.html", context)

@teacher_login_required_html
def assignment(request, abbreviation, code):
    if request.method == "GET":
        course = Course.objects.get(abbreviation=abbreviation)
        assignment = Assignment.objects.get(course=course, code=code)
        questions = Question.objects.filter(assignment=assignment)
        
        if (course is not None and assignment is not None):
            if len(questions) == 0:
                raise Http404
            question_list = []
            for question in questions:
                difficulty = question.difficulty
                data = {
                    'name': question.name,
                    'code' : question.code,
                    'difficulty': difficulty,
                    'n': range(difficulty), 
                    'not_n': range(difficulty,5),
                }
                question_list.append(data)
            context = {
                "course": course,
                "assignment": assignment,
                "questions": question_list,
            }
            return render(request, "teacher/assignment.html", context)
        else:
            raise Http404

@teacher_login_required_html
def question(request, abbreviation, code, as_code):
    if request.method == "GET":
        course = Course.objects.get(abbreviation=abbreviation)
        assignment = Assignment.objects.get(course=course, code=as_code)
        question = Question.objects.get(code=code)
        
        if (course is not None and assignment is not None and question is not None):
            difficulty = question.difficulty
            context = {
                "course": course,
                "assignment": assignment,
                "question": question,
                'difficulty': difficulty,
                'n': range(difficulty), 
                'not_n': range(difficulty,5),
            }
            return render(request, "teacher/question.html", context)
        else:
            raise Http404

@teacher_login_required_html         
def add_testcase(request, as_code, abbreviation, code):
    try:
        course = Course.objects.get(abbreviation=abbreviation)
        problem_object = Question.objects.get(code=code)
        assignment_object = Assignment.objects.get(code=as_code)
        
        context = {
            'course' : course,
            'assignment': assignment_object,
            'question': problem_object,
        }
        
        return render(request, "teacher/add_testcase.html", context)
    except Exception as e:
        print("Error : " + str(e))
        return HttpResponseServerError("Internal Server Error")


def login(request):
    if request.method == "GET":
        return render(request, "teacher/login.html", {})

def superuser_login(request):
    if request.method == "GET":
        return render(request, "teacher/superuser_login.html", {})

def register(request):
    if request.method == "GET":
        return render(request, "teacher/register.html", {})

@login_superuser
def course_register(request):
    if (request.method == "GET"):
        context = {
            "teachers": Teacher.objects.all(),
        }
        return render(request, "teacher/register_course.html", context) 