from django.http import HttpResponse, Http404, HttpResponseServerError
from django.utils.encoding import smart_str
from wsgiref.util import FileWrapper

from api.tasks import *
from api.exceptions import *
from my_App.models import *
from . tasks import *

import csv

def download_file(filename, filepath):
    with open(filepath, 'rb') as file:
        response = HttpResponse(file, content_type='application/force-download')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        response['Content-Length'] = len(response.content)
        # response['X-Sendfile'] = smart_str(filepath)
        return response

@teacher_login_required_html
def get_assignment_csv(request, abbreviation, as_code):
    try:
        course = Course.objects.get(abbreviation=abbreviation)
        assignment = Assignment.objects.get(course=course, code=as_code)
        teacher = User.objects.get(username = request.session['user']['username']).teacher
        
        filename = course.abbreviation + '_' + assignment.code + ".csv"
        filepath = "csv/" + filename
        
        if (teacher not in course.teacher.all()):
            return JsonError(status_code=403, message="Teacher not an instructor of this course!")
        else:
            questions = Question.objects.filter(assignment=assignment)
            if len(questions) == 0:
                raise NoQuestionException
            columns = ["Roll No.", "Name"]
            students = Profile.objects.filter(course=course)
            for question in questions:
                columns.append(f"{question.code}")
            
            with open(filepath, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(columns)
                for student in students:
                    row = [f"{student.roll_no}", f"{student.user.get_full_name()}"]
                    for question in questions:
                        try:
                            submission = Submission.objects.get(student=student, question=question)
                            row.append("Yes")
                        except Submission.DoesNotExist:
                            row.append("No")
                    writer.writerow(row)
            return download_file(filename, filepath)
    except Course.DoesNotExist:
        raise Http404
    except Assignment.DoesNotExist:
        raise Http404
    except NoQuestionException:
        raise Http404
    except Exception as e:
        print("Error : " + str(e))
        return HttpResponseServerError("Internal Server Error")

@teacher_login_required_html
def get_question_csv(request, abbreviation, as_code, code):
    try:
        course = Course.objects.get(abbreviation=abbreviation)
        assignment = Assignment.objects.get(course=course, code=as_code)
        question = Question.objects.get(assignment=assignment, code=code)
        teacher = User.objects.get(username = request.session['user']['username']).teacher
        
        filename = course.abbreviation + '_' + assignment.code + '_' + question.code + ".csv"
        filepath = "csv/" + filename
        
        if (teacher not in course.teacher.all()):
            return JsonError(status_code=403, message="Teacher not an instructor of this course!")
        else:
            students = Profile.objects.filter(course=course)
            with open(filepath, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Roll No", "Name", "Completed", "Time"])
                for student in students:
                    try:
                        submission = Submission.objects.get(student=student, question=question)
                        writer.writerow([f"{student.roll_no}", f"{student.user.get_full_name()}", "Yes", \
                        f"{submission.time_of_submission}"])
                    except Submission.DoesNotExist:
                        writer.writerow([f"{student.roll_no}", f"{student.user.get_full_name()}", "No", None])
            return download_file(filename, filepath)
    except Course.DoesNotExist:
        raise Http404
    except Assignment.DoesNotExist:
        raise Http404
    except Question.DoesNotExist:
        raise Http404
    except Exception as e:
        print("Error : " + str(e))
        return HttpResponseServerError("Internal Server Error")