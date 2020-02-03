from django.shortcuts import render
from api.tasks import *
from api.exceptions import *
from django.core.serializers import serialize
from django.contrib.auth import authenticate
from . models import *
from . tasks import *

import subprocess

# Create your views here.
@teacher_login_required
def index(request):
    if request.method == "GET":
        try:
            teacher_username = request.session['user']['username']
            teacher = User.objects.get(username=teacher_username).teacher
            courses = [] 
            for course in Course.objects.filter(teacher=teacher):
                courses.append({
                    'name': course.name, 
                    'code': course.code,
                    'id': course.id,
                    'abbreviation': course.abbreviation,
                })
            if len(courses) == 0:
                raise NoCourseException
            context = {
                "courses": courses,
            }
            return JsonHandler(request, context)
        except NoCourseException:
            return JsonError(status_code=400, message="No courses taught!")
        except Exception as e:
            print("Error : " + str(e))
            return JsonError(status_code=500, message=f"Unknown Error")
    else:
        return JsonError(status_code=400, message=f"Only POST allowed!")

@teacher_login_required
def set_assignment(request, abbreviation):
    if request.method == "POST":
        try:
            course_name = request.POST['course_name']
            name = request.POST['name']
            code = request.POST['code']
            course = Course.objects.get(abbreviation=abbreviation, name=course_name)
            assignment = Assignment(name=name, course=course, code=code)
            assignment.save() 
            return JsonHandler(request, context = {})
        except Course.DoesNotExist:
            return JsonError(status_code=400, message="No such course taught!")
        except Exception as e:
            print("Error : " + str(e))
            return JsonError(status_code=500, message=f"Unknown Error")
    else:
        return JsonError(status_code=400, message=f"Only POST allowed!")

@teacher_login_required
def set_question(request, abbreviation, code):
    if request.method == "POST":
        try:
            course_name = request.POST['course_name']
            assignment_name = request.POST['assignment_name']
            course = Course.objects.get(abbreviation=abbreviation, name=course_name)
            assignment = Assignment.objects.get(course=course, name=assignment_name, code=code)
            name = request.POST['name']
            code = request.POST['code']
            problem_desc = request.POST['problem_desc']
            sample_input = request.POST['sample_input']
            sample_output = request.POST['sample_output']
            discussions = request.POST['discussions']
            difficulty = request.POST['difficulty']
            question = Question(assignment=assignment, name=name, code=code, problem_desc=problem_desc, 
            sample_input=sample_input, sample_output=sample_output, discussions=discussions, difficulty=difficulty)
            question.save()
            return JsonHandler(request, context = {})
        except Course.DoesNotExist:
            return JsonError(status_code=400, message="No such course taught!")
        except Assignment.DoesNotExist:
            return JsonError(status_code=400, message="No such assignment present!")
        except Exception as e:
            print("Error : " + str(e))
            return JsonError(status_code=500, message=f"Unknown Error")
    else:
        return JsonError(status_code=400, message=f"Only POST allowed!")

@teacher_login_required
def course(request, abbreviation):
    if request.method == "GET":
        try:
            course = Course.objects.get(abbreviation=abbreviation)
            assignments = Assignment.objects.filter(course=course)
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

@teacher_login_required
def assignment(request, abbreviation, code):
    if request.method == "GET":
        try:
            course = Course.objects.get(abbreviation=abbreviation)
            assignment = Assignment.objects.get(course=course, code=code)
            questions = Question.objects.filter(assignment=assignment)
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

def register(request):
    if request.method == "POST":
        try:
            username = request.POST['username']
            password = request.POST['password']
            first = request.POST['first']
            last = request.POST['last']
            email = request.POST['email']
            user = User.objects.create_user(username=username, password=password, first_name=first, last_name=last, email=email)
            try:
                profile = Teacher(user=user)
                profile.save()
                return JsonHandler(request, context={'response':"Success"}, user_show = False)
            except Exception as e:
                user.delete()
                return JsonError(status_code=400, message=str(e))
        except Exception as e:
            print("Error : " + str(e))
            return JsonError(status_code=500, message=f"Unknown Error")
    else:
        return JsonError(status_code=400, message=f"Only POST allowed!")

@login_superuser
def course_register(request):
    if request.method == "GET":
        teachers = []
        for teacher in Teacher.objects.all():
            teachers.append({"name" : "Prof. " + teacher.user.get_full_name(), "id" : teacher.id})
        context = {
            "teachers": teachers,
        }
        return JsonHandler(request, context, user_show = False)
    elif request.method == "POST":
        try:
            name = request.POST['name']
            code = request.POST['code']
            teacher_id = request.POST['teacher']
            abbreviation = request.POST['abbreviation']
            teacher = Teacher.objects.get(id=teacher_id)
            try:
                course = Course(name=name, code=code, abbreviation=abbreviation)
                course.save()
                course.teacher.add(teacher)
                subprocess.Popen(f"mkdir data/{abbreviation}", shell=True)
                return JsonHandler(request, context={'response':"Success"}, user_show = False)
            except Exception as e:
                return JsonError(status_code=400, message=str(e))
        except Exception as e:
            print("Error : " + str(e))
            return JsonError(status_code=500, message=f"Unknown Error")
    else:
        return JsonError(status_code=400, message=f"Only POST allowed!")

def login(request):
    if request.method == "POST":
        try:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username = username, password = password)
            if user is not None:
                context = {
                    "username" : user.username,
                    "full_name" : "Prof. " + user.get_full_name(),
                    "type" : "Teacher",
                }
                request.session['user'] = context
                return JsonHandler(request, context={'response':"Success"})
            else:
                request.session['user'] = None
                return JsonError(status_code=400, message=f"Authentication Error!")
        except Exception as e:
            print("Error : " + str(e))
            return JsonError(status_code=500, message=f"Unknown Error")
    else:
        return JsonError(status_code=400, message=f"Only POST allowed!")

# Handles student enrollment
@login_superuser
def add_student_to_course(request):
    if request.method == "POST":
        try:
            course = Course.objects.get(abbreviation=request.POST['course_abbreviation'])
            student = Profile.objects.get(id=request.POST['student_id'])
            student.course.add(course)
            subprocess.Popen(f"mkdir data/{course.abbreviation}/{student.user.username}", shell=True)
            return JsonHandler(request, context={'response':"Success"})
        except Course.DoesNotExist:
            return JsonError(status_code=400, message="No such course taught!")
        except Profile.DoesNotExist:
            return JsonError(status_code=400, message="No such student!")
        except Exception as e:
            print("Error : " + str(e))
            return JsonError(status_code=500, message=f"Unknown Error!")
    else:
        return JsonError(status_code=400, message=f"Only POST allowed!") 

@teacher_login_required
def add_testcase(request, as_code, abbreviation, code):
    if request.method == "GET":
        try:
            course = Course.objects.get(abbreviation=abbreviation)
            question = Question.objects.get(code=code)
            assignment = Assignment.objects.get(code=as_code)
            
            course = {
                "name" : course.name,
                "abbreviation" : course.abbreviation,
                "code": course.code,
                }
            assignment = {
                "name" : assignment.name,
                "code" : assignment.code,
            }
            
            testcases = TestCase.objects.filter(question=question)
            testcase_list = []
            
            for testcase in testcases:
                testcase_list.append({
                    'input_case' : testcase.input_case,
                    'output_case' : testcase.output_case,
                    'description': testcase.description,
                })
            
            question = {
                'name': question.name,
                'code' : question.code,
                'difficulty': question.difficulty,
            }
            
            context = {
                'course': course,
                'assignment': assignment,
                'question': question,
                'testcases': testcase_list,
            }
        
            return JsonHandler(request, context)
        except Course.DoesNotExist:
            return JsonError(status_code=400, message="No such course taught!")
        except Assignment.DoesNotExist:
            return JsonError(status_code=400, message="No such assignment present!")
        except Question.DoesNotExist:
            return JsonError(status_code=400, message="No such question present!")
        except Exception as e:
            print("Error : " + str(e))
            return JsonError(status_code=500, message=f"Unknown Error!")
    if request.method == "POST":
        try:
            course = Course.objects.get(abbreviation=abbreviation)
            question = Question.objects.get(code=code)
            assignment = Assignment.objects.get(code=as_code)
            
            description = request.POST['testcase_desc']
            input_case = request.POST['input_case']
            output_case = request.POST['output_case']
            
            tc = TestCase(question=question, description=description, input_case=input_case, output_case=output_case)
            tc.save()
            
            return JsonHandler(request, context={'response':"Success"})
        except Course.DoesNotExist:
            return JsonError(status_code=400, message="No such course taught!")
        except Assignment.DoesNotExist:
            return JsonError(status_code=400, message="No such assignment present!")
        except Question.DoesNotExist:
            return JsonError(status_code=400, message="No such question present!")
        except Exception as e:
            print("Error : " + str(e))
            return JsonError(status_code=500, message=f"Unknown Error!")
    else:
        return JsonError(status_code=400, message=f"Only POST and GET allowed!")

def superuser_login(request):
    if request.method == "POST":
        try:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username = username, password = password)
            if user is not None:
                context = {
                    "username" : user.username,
                    "type" : "Superuser",
                }
                request.session['user'] = context
                return JsonHandler(request, context={'response':"Success"})
            else:
                request.session['user'] = None
                return JsonError(status_code=400, message=f"Authentication Error!")
        except Exception as e:
            print("Error : " + str(e))
            return JsonError(status_code=500, message=f"Unknown Error")
    else:
        return JsonError(status_code=400, message=f"Only POST allowed!")

@teacher_login_required
def question(request, abbreviation, as_code, code):
    try:
        course = Course.objects.get(abbreviation=abbreviation)
        assignment_object = Assignment.objects.get(code=as_code)
        problem_object = Question.objects.get(assignment=assignment_object, code=code)
                
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