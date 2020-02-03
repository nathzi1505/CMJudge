from django.http import JsonResponse, Http404
from django.conf import settings
from django.contrib.auth import authenticate
from . exceptions import *
from my_App.models import *
from functools import wraps
import datetime

def JsonError(status_code, message):
    context = {
        'status':status_code,
        'response':message,
    }
    return JsonAccessControlModifier(context)
    
def JsonHandler(request, context, user_show = True, submission_show = True):
    context["status"] = 200
    if user_show == True:
        context["user"] = request.session['user']
    if submission_show == False:
        context['user'].pop('submissions')
    return JsonAccessControlModifier(context)

def JsonAccessControlModifier(context):
    # response = JsonResponse(context, status = context["status"])
    response = JsonResponse(context)
    response["Access-Control-Allow-Origin"] = "http://localhost:3000"
    response["Access-Control-Allow-Credentials"] = "true"
    response["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response

def GetCompiler(lang):
    if lang == 'C':
        return "gcc"
    elif lang == 'C++':
        return "g++"

def GetExtension(lang):
    if lang == 'C':
        return ".c"
    elif lang == 'C++':
        return ".cpp"

def GetTimeStamp():
    time_stamp = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
    new_time_stamp = ""
    for ch in time_stamp:
        if ch == ' ':
            ch = '_'
        new_time_stamp = new_time_stamp + ch
    return new_time_stamp

def Write2File(text, location, lang):
    filelocation = location + GetExtension(lang)
    with open(filelocation, "w") as file:
        file.write(text)
    return filelocation

def RefreshUserDetails(request):
    user = User.objects.get(username=request.session['user']['username'])
    if user is not None:
        profile = user.profile
        student_submissions = Submission.objects.filter(student=profile).order_by('-time_of_submission')[0:5]
        student_submissions_list = []
        for submission in student_submissions:
            problem_object = submission.question
            assignment_object = problem_object.assignment
            course = assignment_object.course
            course = {
                'name': course.name, 
                'code': course.code,
                'id': course.id,
                'abbreviation': course.abbreviation,
            }
            assignment_object = {
                'code': assignment_object.code,
                'name': assignment_object.name,
            }    
            problem_object = {
                'name' : problem_object.name,
                'code' : problem_object.code,
            }
            student_submissions_list.append({
                'time_of_submission': submission.time_of_submission.timestamp(),
                'question': problem_object,
                'assignment' : assignment_object,
                'course': course,
            })
        context = {
            "username" : profile.user.username,
            "full_name" : profile.user.get_full_name(),
            "roll_no" : profile.roll_no,
            "type": "Student",
            "submissions" : student_submissions_list
        }
        request.session['user'] = context
        return context
    else:
        request.session['user'] = None
        raise UserAuthenticationError
            
def UserAuthenticate(request, username, password):
    user = authenticate(username = username, password = password)
    if user is not None:
        profile = user.profile
        student_submissions = Submission.objects.filter(student=profile).order_by('-time_of_submission')[0:5]
        student_submissions_list = []
        for submission in student_submissions:
            problem_object = submission.question
            assignment_object = problem_object.assignment
            course = assignment_object.course
            course = {
                'name': course.name, 
                'code': course.code,
                'id': course.id,
                'abbreviation': course.abbreviation,
            }
            assignment_object = {
                'code': assignment_object.code,
                'name': assignment_object.name,
            }    
            problem_object = {
                'name' : problem_object.name,
                'code' : problem_object.code,
            }
            student_submissions_list.append({
                'time_of_submission': submission.time_of_submission.timestamp(),
                'question': problem_object,
                'assignment' : assignment_object,
                'course': course,
            })
        context = {
            "username" : profile.user.username,
            "full_name" : profile.user.get_full_name(),
            "roll_no" : profile.roll_no,
            "type": "Student",
            "submissions" : student_submissions_list
        }
        request.session['user'] = context
        return context
    else:
        request.session['user'] = None
        raise UserAuthenticationError
    
def login_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        try:
            if (request.session['user'] and request.session['user']['type'] == 'Student') or User.objects.get(username=request.session['user']['username']).is_superuser == True:
                RefreshUserDetails(request)
                return func(request, *args, **kwargs)
            else:
                return JsonError(403, "Forbidden")
        except KeyError:
            return JsonError(403, "Forbidden")
        except Http404:
            raise Http404
        except Exception as e:
            print("Error : {}".format(str(e)))
            return JsonError(500, "Unknown Error")
    return wrapper
    
def login_superuser(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        try:
            if request.session['user'] and User.objects.get(username=request.session['user']['username']).is_superuser == True:
                return func(request, *args, **kwargs)
            else:
                return JsonError(403, "Forbidden")
        except KeyError:
            return JsonError(403, "Forbidden")
        except Http404:
            raise Http404
        except Exception as e:
            print("Error : {}".format(str(e)))
            return JsonError(500, "Unknown Error")
    return wrapper