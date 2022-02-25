from django.http import JsonResponse
from API.models import Roles, Usuario
import jwt, datetime

def tokenValidate(fn):
    def jwtValidator ( *args, **kw_args):
        try:
            token = args[1].META['HTTP_X_TOKEN_ACCESS']
            data = jwt.decode(token, 'secret_key', algorithms="HS256")
            user = list(Roles.objects.filter(id=data['id']).values())
            if len(user>0):
                pass
            else:
                return JsonResponse({ "message": "invalid token"})
        except:
            return JsonResponse({ "message": "invalid token"})
        return fn(*args)
    return jwtValidator

def isAdmin(fn):
    def adminValidate(*args, **kw_args):
        token = args[1].META['HTTP_X_TOKEN_ACCESS']
        data = jwt.decode(token, 'secret_key', algorithms="HS256")
        role = list(Roles.objects.filter(id=data['role_id']).values())
        if role['nombre']=='Admin':
            pass
        else:
            return JsonResponse({ "message": "You aren't allowed to stay here"})
        return fn(*args)
    return adminValidate