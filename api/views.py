from django.shortcuts import render
from django.http import JsonResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from my_App.models import *
from . tasks import *
from . exceptions import *
from . execute import execute
import datetime
import subprocess
import os

# Handles the index api
@login_required 
def index(request):
    try:
        username = request.session['user']['username']
        student = User.objects.get(username=username).profile
        course_list = []
        for course in student.course.all():
            course_list.append({
                'name': course.name,
                'abbreviation': course.abbreviation,
                'code': course.code,
            })
        if len(course_list) == 0:
            raise NoCourseException
        context = {
            "courses": course_list,
        }
        return JsonHandler(request, {"response" : context})
    except NoCourseException:
        return JsonError(status_code=404, message="No Course exists!")
    except Assignment.DoesNotExist:
        return JsonError(status_code=404, message="No Assignment exists!")
    except Exception as e:
        print("Error : " + str(e))
        return JsonError(status_code=500, message="Unknown Error")

# Handles the assignment api
@login_required
def assignment(request, abbreviation, as_code):
    if request.method == "GET":
        try:
            course = Course.objects.get(abbreviation=abbreviation)
            assignment = Assignment.objects.get(course=course, code=as_code)
            questions = Question.objects.filter(assignment=assignment)
            
            if (course not in User.objects.get(username=request.session['user']['username']).profile.course.all()):
                return JsonError(status_code=400, message=f"Not enrolled in the course")
            
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
                if len(questions) == 0:
                    raise NoQuestionException
                question_list = []
                for question in questions:
                    data = {
                        'name': question.name,
                        'code' : question.code,
                        'difficulty': question.difficulty,
                    }
                    question_list.append(data)
                context = {
                    "course": course,
                    "assignment": assignment,
                    "questions": question_list,
                }
                return JsonHandler(request, context)
        except Course.DoesNotExist:
            return JsonError(status_code=400, message="No such course taught!")
        except Assignment.DoesNotExist:
            return JsonError(status_code=400, message="No such assignment present!")
        except NoQuestionException:
            return JsonError(status_code=400, message="No assignments present!")
        except Exception as e:
            print("Error : " + str(e))
            return JsonError(status_code=500, message=f"Unknown Error")
    else:
        return JsonError(status_code=400, message=f"Only GET allowed!")
        
# Handles the course api
@login_required
def course(request, abbreviation):
    if request.method == "GET":
        try:
            course = Course.objects.get(abbreviation=abbreviation)
            assignments = Assignment.objects.filter(course=course)
            
            if (course not in User.objects.get(username=request.session['user']['username']).profile.course.all()):
                return JsonError(status_code=400, message=f"Not enrolled in the course")
                
            if len(assignments) == 0:
                raise NoAssignmentException
            course = {
                'name': course.name, 
                'code': course.code,
                'id': course.id,
                'abbreviation': course.abbreviation,
            }
            assignment_list= []
            for assignment in assignments:
                assignment_list.append({
                    'code': assignment.code,
                    'name': assignment.name,
                })
            context = {
                "course": course,
                "assignments": assignment_list,
            }
            return JsonHandler(request, context)
        except Course.DoesNotExist:
            return JsonError(status_code=400, message="No such course taught!")
        except Assignment.DoesNotExist:
            return JsonError(status_code=400, message="No such assignment present!")
        except NoAssignmentException:
            return JsonError(status_code=400, message="No assignments present!")
        except Exception as e:
            print("Error : " + str(e))
            return JsonError(status_code=500, message=f"Unknown Error")
    else:
        return JsonError(status_code=400, message=f"Only GET allowed!")

# Handles the question api
@login_required
def question(request, abbreviation, as_code, code):
    try:
        course = Course.objects.get(abbreviation=abbreviation)
        assignment_object = Assignment.objects.get(code=as_code)
        problem_object = Question.objects.get(assignment=assignment_object, code=code)
        
        if (course not in User.objects.get(username=request.session['user']['username']).profile.course.all()):
                return JsonError(status_code=400, message=f"Not enrolled in the course")
                
        difficulty = problem_object.difficulty
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
        context = {
            'course': course,
            'assignment': assignment_object,
            'name' : problem_object.name,
            'code' : problem_object.code,
            'problem_desc': problem_object.problem_desc,
            'sample_input': problem_object.sample_input,
            'sample_output': problem_object.sample_output,
            'discussions': problem_object.discussions,
            'difficulty': difficulty,
        }
        return JsonHandler(request, context)
    
    except Course.DoesNotExist:
        return JsonError(status_code=400, message="No such course taught!")
    except Assignment.DoesNotExist:
        return JsonError(status_code=404, message=f"No such assignment present!")
    except Question.DoesNotExist:
        return JsonError(status_code=404, message=f"No such question present!")
    except Exception as e:
        print("Error : " + str(e))
        return JsonError(status_code=500, message=f"Unknown Error!")

# Handles the submission api
@login_required
def submit(request, abbreviation, as_code, code):
    if request.method == "POST": 
        try:
            course = Course.objects.get(abbreviation=abbreviation)
            assignment_object = Assignment.objects.get(code=as_code)
            problem_object = Question.objects.get(assignment=assignment_object, code=code)
            username = request.session['user']['username']
            
            if (course not in User.objects.get(username=request.session['user']['username']).profile.course.all()):
                return JsonError(status_code=400, message=f"Not enrolled in the course")
            
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
        
            file = request.FILES['source_code']
            language = request.POST['lang']
            location = settings.MEDIA_ROOT + f"{course['abbreviation']}/{username}/"
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
                return JsonError(status_code=status_code, message=response)
            else:
                problem_object = {
                'name' : problem_object.name,
                'code' : problem_object.code,
                }
                context = {
                    'course': course,
                    'assignment_object': assignment_object,
                    'problem_object': problem_object,
                    'response': response,
                }
            return JsonHandler(request, context)
        except Course.DoesNotExist:
            return JsonError(status_code=400, message="No such course taught!")
        except Assignment.DoesNotExist:
            return JsonError(status_code=404, message=f"No such assignment present!")
        except Question.DoesNotExist:
            return JsonError(status_code=404, message=f"No such question present!")
        except MultiValueDictKeyError:
            return JsonError(status_code=400, message=f"File not found!")
        except Exception as e:
            print("Error : " + str(e))
            return JsonError(status_code=500, message=f"Unknown Error!")
    else:
        return JsonError(status_code=400, message=f"Only POST allowed!")

# Handles the submit-text api
@login_required
def submit_text(request, as_code, abbreviation, code):
    if request.method == "POST":
        try:
            course = Course.objects.get(abbreviation=abbreviation)
            problem_object = Question.objects.get(code=code)
            assignment_object = Assignment.objects.get(code=as_code)
            username=request.session['user']['username']
            
            if (course not in User.objects.get(username=request.session['user']['username']).profile.course.all()):
                return JsonError(status_code=400, message=f"Not enrolled in the course")
            
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
            
            text = request.POST['source_code']
            language = request.POST['lang']
            if len(text) == 0:
                raise NoTextError
                
            location = settings.MEDIA_ROOT + f"{course['abbreviation']}/{username}/"
            
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
                return JsonError(status_code=status_code, message=response)
            else:
                problem_object = {
                'name' : problem_object.name,
                'code' : problem_object.code,
                }
                context = {
                    'course': course,
                    'assignment_object': assignment_object,
                    'problem_object': problem_object,
                    'response': response,
                }
            return JsonHandler(request, context)
        except Course.DoesNotExist:
            return JsonError(status_code=400, message="No such course taught!")
        except Assignment.DoesNotExist:
            return JsonError(status_code=404, message=f"No such assignment present!")
        except Question.DoesNotExist:
            return JsonError(status_code=404, message=f"No such question present!")
        except NoTextError:
            return JsonError(status_code=400, message=f"Text not found!")
        except Exception as e:
            print("Error : " + str(e))
            return JsonError(status_code=500, message=f"Unknown Error!")
    else:
        return JsonError(status_code=400, message=f"Only POST allowed!")

# Handles the register api
def register(request):
    if request.method == "POST":
        try:
            username = request.POST['username']
            password = request.POST['password']
            roll_no = request.POST['roll_no']
            first = request.POST['first']
            last = request.POST['last']
            user = User.objects.create_user(username=username, password=password, first_name=first, last_name=last)
            try:
                profile = Profile(user=user, roll_no=roll_no)
                profile.save()
                return JsonHandler(request, context={'response':"Success"}, user_show = False)
            except Exception as e:
                user.delete()
                return JsonError(status_code=400, message=str(e))
        except Exception as e:
            print("Error : " + str(e))
            return JsonError(status_code=400, message=str(e))
            
    else:
        return JsonError(status_code=400, message=f"Only POST allowed!")

# Handles the login api
def login(request):
    if request.method == "POST":
        try:
            username = request.POST['username']
            password = request.POST['password']
            UserAuthenticate(request, username, password)
            return JsonHandler(request, context={'response':"Success"})
        except UserAuthenticationError:
            return JsonError(status_code=400, message=f"Authentication Error!")
        except Exception as e:
            print("Error : " + str(e))
            return JsonError(status_code=500, message=f"Unknown Error!")
    else:
        return JsonError(status_code=400, message=f"Only POST allowed!")

# Handles the logout api
@login_required
def logout(request):
    if request.method == "POST":
        request.session['user'] = None
        return JsonHandler(request, context={'response':"Success"})

# Handles the successful student submissions     
@login_required
def get_submissions(request):
    if request.method == "GET":
        try:
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
                    'time_of_submission': submission.time_of_submission.timestamp()
                })
                
            if len(submissions_list) == 0:
                raise NoSubmissionError
            return JsonHandler(request, context = {'submissions': submissions_list}, submission_show = False)
        except NoSubmissionError:
            return JsonError(status_code=400, message=f"No Successful Submission made!")
        except Exception as e:
            print("Error : " + str(e))
            return JsonError(status_code=500, message=f"Unknown Error!")
    else:
        return JsonError(status_code=400, message=f"Only GET allowed!")