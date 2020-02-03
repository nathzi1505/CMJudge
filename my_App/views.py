from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseServerError
from django.core.exceptions import PermissionDenied
from django.core.files.storage import FileSystemStorage
from . models import *
from api.tasks import *
from api.execute import *

import os

class CompileError(Exception):
    pass

def login_required_view(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        try:
            if (request.session['user'] and request.session['user']['type'] == 'Student') or User.objects.get(username=request.session['user']['username']).is_superuser == True:
                return func(request, *args, **kwargs)
            else:
                raise PermissionDenied
        except Http404:
            raise Http404
        except PermissionDenied:
            raise PermissionDenied
        except KeyError:
            raise PermissionDenied
        except Exception as e:
            print("Error : " + str(e))
            return HttpResponseServerError("Internal Server Error")
    return wrapper

# Handles the index page
@login_required_view
def index(request):
    if request.method == "GET":
        try:
            username = request.session['user']['username']
            student = User.objects.get(username=username).profile
            context = {
                "courses": student.course.all(),
            }
            return render(request, "my_App/index.html", context)
        except Exception as e:
            print("Error : " + str(e))
            return HttpResponseServerError("Internal Server Error")
        
# Handles the course page
@login_required_view
def course(request, abbreviation):
    if request.method == "GET":
        course = Course.objects.get(abbreviation=abbreviation)
        assignments = Assignment.objects.filter(course=course)
        
        if (course not in User.objects.get(username=request.session['user']['username']).profile.course.all()):
            raise PermissionDenied
        
        if len(assignments) == 0:
            raise Http404
        context = {
            "course": course,
            "assignments": assignments,
        }
        return render(request, "my_App/course.html", context)

# Handles the assignment page
@login_required_view
def assignment(request, abbreviation, as_code):
    try:
        course = Course.objects.get(abbreviation=abbreviation)
        assignment = Assignment.objects.get(code=as_code)
        problems = Question.objects.filter(assignment_id=assignment.id)
        
        if (course not in User.objects.get(username=request.session['user']['username']).profile.course.all()):
            raise PermissionDenied
        
        if len(problems) == 0:
            raise Exception
        context = []
        for problem in problems:
            difficulty = problem.difficulty
            data = {
                'name' : problem.name,
                'code' : problem.code,
                'difficulty': difficulty,
                'n': range(difficulty), 
                'not_n': range(difficulty,5),
            }
            context.append(data)
        context = {
            "course": course,
            "assignment": assignment,
            "questions": context,
        }
        return render(request, "my_App/assignment.html", context)
    except PermissionDenied:
        raise PermissionDenied
    except Exception as e:
        print("Error : " + str(e))
        return HttpResponseServerError("Internal Server Error")

# Handles the question page
@login_required_view
def question(request, as_code, abbreviation, code):
    try:
        course = Course.objects.get(abbreviation=abbreviation)
        problem_object = Question.objects.get(code=code)
        assignment_object = Assignment.objects.get(code=as_code)
        
        if (course not in User.objects.get(username=request.session['user']['username']).profile.course.all()):
            raise PermissionDenied
            
        difficulty = problem_object.difficulty
        context = {
            'course': course,
            'code' : problem_object.code,
            'name' : problem_object.name,
            'assignment': assignment_object,
            'problem_desc': problem_object.problem_desc,
            'sample_input': problem_object.sample_input,
            'sample_output': problem_object.sample_output,
            'discussions': problem_object.discussions,
            'difficulty': difficulty,
            'n': range(difficulty), 
            'not_n': range(difficulty,5),
        }
        return render(request, "my_App/problem_page.html", context)
    except PermissionDenied:
        raise PermissionDenied
    except Exception as e:
        print("Error : " + str(e))
        return HttpResponseServerError("Internal Server Error")

# Handles the submission  page
@login_required_view
def submit(request, as_code, abbreviation, code):
    if request.method == "GET": 
        try:
            course = Course.objects.get(abbreviation=abbreviation)
            problem_object = Question.objects.get(code=code)
            assignment_object = Assignment.objects.get(code=as_code)
            if not problem_object.assignment.id == assignment_object.id:
                raise ValueError
            
            if (course not in User.objects.get(username=request.session['user']['username']).profile.course.all()):
                raise PermissionDenied
            
            difficulty = problem_object.difficulty
            context = {
                'course': course,
                'code' : problem_object.code,
                'name' : problem_object.name,
                'assignment': assignment_object,
                'difficulty': difficulty,
                'n': range(difficulty), 
                'not_n': range(difficulty,5),
            }
            try :
                if request.GET['text'] == 'True':
                    return render(request, "my_App/submit_text.html", context)
            except :
                return render(request, "my_App/submit.html", context)
        except PermissionDenied:
            raise PermissionDenied
        except Exception as e:
            print("Error : " + str(e))
            return HttpResponseServerError("Internal Server Error")
    elif request.method == "POST": 
        try:
            course = Course.objects.get(abbreviation=abbreviation)
            problem_object = Question.objects.get(code=code)
            assignment_object = Assignment.objects.get(code=as_code)
            username = request.session['user']['username']
            
            if (course not in User.objects.get(username=request.session['user']['username']).profile.course.all()):
                raise PermissionDenied
            
            if not problem_object.assignment.id == assignment_object.id:
                raise ValueError
            context = {
                'response' : "Success"
            }
            
            file = request.FILES['source_code']
            language = request.POST['lang']
            location = settings.MEDIA_ROOT + f"{course.abbreviation}/{username}/"
            filename = f"{problem_object.code}" + GetExtension(language)
            
            if os.path.exists(location + filename):
                os.remove(location + filename)
            
            fs = FileSystemStorage(location = location)
            file = location + fs.save(filename, file)
            
            test_cases = TestCase.objects.filter(question=problem_object).all()
            
            cases = []
            for i in range(len(test_cases)):
                cases.append((test_cases[i].input_case, test_cases[i].output_case, test_cases[i].description))
            
            status_code, response = execute(request.session['user'], problem_object, file, GetCompiler(request.POST['lang']), cases)
            if not status_code == 200:
                raise CompileError
            else:
                context = {
                    'course': course,
                    'assignment': assignment_object,
                    'name' : problem_object.name,
                    'response': response,
                    'code' : code,
                }
            return render(request, "my_App/results.html", context)
        except CompileError:
            return HttpResponseServerError("Compilation Error")
        except PermissionDenied:
            raise PermissionDenied
        except Exception as e:
            print("Error : " + str(e))
            return HttpResponseServerError("Internal Server Error")

@login_required_view
def results(request, as_code, code, abbreviation):
    if request.method == "POST":
        try:
            course = Course.objects.get(abbreviation=abbreviation)
            problem_object = Question.objects.get(code=code)
            assignment_object = Assignment.objects.get(code=as_code)
            username=request.session['user']['username']
            
            if (course not in User.objects.get(username=username).profile.course.all()):
                raise PermissionDenied
            
            text = request.POST['source_code']
            language = request.POST['lang']
            if len(text) == 0:
                raise NoTextError
                
            location = settings.MEDIA_ROOT + f"{course.abbreviation}/{username}/"
            
            filename = f"{problem_object.code}" + GetExtension(language)
            
            if os.path.exists(location + filename):
                os.remove(location + filename)
            
            file = Write2File(text, location + f"{problem_object.code}", language)
            
            test_cases = TestCase.objects.filter(question=problem_object).all()
            
            cases = []
            for i in range(len(test_cases)):
                cases.append((test_cases[i].input_case, test_cases[i].output_case, test_cases[i].description))
            
            status_code, response = execute(request.session['user'], problem_object, file, GetCompiler(request.POST['lang']), cases)
            
            if not status_code == 200:
                raise CompileError
            else:
                context = {
                    'course': course,
                    'assignment': assignment_object,
                    'response': response,
                    'code' : code, 
                    'name' : problem_object.name,
                }
            return render(request, "my_App/results.html", context)
        except CompileError:
            return HttpResponseServerError("Compilation Error")
        except PermissionDenied:
            raise PermissionDenied
        except Exception as e:
            print("Error : " + str(e))
            return HttpResponseServerError("Internal Server Error")

# Handles the registration  page
def register(request):
    if request.method == "GET":
        context = {}
        return render(request, "my_App/register.html", context)

# Handles the login  page
def login(request):
    if request.method == "GET":
        context = {}
        return render(request, "my_App/login.html", context)

# Handles the logout page
@login_required_view
def logout(request):
    if request.method == "GET":
        del request.session['user']
        return render(request, "my_App/logout.html")

# Handles the addition of student to course
@login_superuser
def add_student_to_course(request):
    courses = Course.objects.all()
    students = Profile.objects.all()
    context = {
        'courses': courses,
        'students': students,
    }
    if request.method == "GET":
        return render(request, "my_App/add_student_to_course.html", context)
        
# Handles the list of submissions
@login_required_view
def get_submissions(request):
    username = request.session['user']['username']
    student = User.objects.get(username=username).profile
    submissions = Submission.objects.filter(student=student)
    submissions_list = []
    
    for submission in submissions:
        question = submission.question
        assignment = question.assignment
        course = assignment.course
        
        course = {
                'name': course.name, 
                'code': course.code,
                'id': course.id,
                'abbreviation': course.abbreviation,
        }
        assignment = {
            'code': assignment.code,
            'name': assignment.name,
        } 
        question = {
                'name' : question.name,
                'code' : question.code,
        }
        
        submissions_list.append({
            'course': course,
            'assignment': assignment,
            'question': question,
            'time_of_submission': submission.time_of_submission
        })
        
    if len(submissions_list) == 0:
        raise Http404
    
    context = {
        'submissions': submissions_list,
    }
    
    return render(request, "my_App/submissions.html", context)

