from api.tasks import *
from django.http import HttpResponseServerError, Http404
from django.core.exceptions import PermissionDenied

def teacher_login_required_html(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        try:
            if (request.session['user'] and request.session['user']['type'] == 'Teacher') or User.objects.get(username=request.session['user']['username']).is_superuser == True:
                return func(request, *args, **kwargs)
            else:
                raise PermissionDenied
        except Http404:
            raise Http404
        except KeyError:
            raise PermissionDenied
        except PermissionDenied:
            raise PermissionDenied
        except Exception as e:
            print("Error : {}".format(str(e)))
            return HttpResponseServerError('Internal Server Error')
    return wrapper

def teacher_login_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        try:
            if (request.session['user'] and request.session['user']['type'] == 'Teacher') or User.objects.get(username=request.session['user']['username']).is_superuser == True:
                return func(request, *args, **kwargs)
            else:
                return JsonError(403, "Forbidden")
        except KeyError:
            return JsonError(403, "Forbidden")
        except Exception as e:
            print("Error : {}".format(str(e)))
            return JsonError(500, "Unknown Error")
    return wrapper
    