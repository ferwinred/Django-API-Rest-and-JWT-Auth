from asyncio.windows_events import NULL
from xml.dom.minidom import Document
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import jwt, datetime
from API.models import Roles, Usuario
from passlib.context import CryptContext
from .decorators import tokenValidate, isAdmin

contexto= CryptContext(
    schemes=['pbkdf2_sha256'],
    default='pbkdf2_sha256',
    pbkdf2_sha256__default_rounds=30000
)

# Create your views here.
class RegisterView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        data = json.loads(request.body)
        encryptPass = contexto.hash(data['password'])
        try:
            Usuario.objects.create(nombres=data['nombres'], apellidos=data['apellidos'], dni=data['dni'], tipo_dni=data['tipo_dni'], email=data['email'], password=encryptPass, hobbies=data['hobbies'], role_id='1' )
            return JsonResponse({'message': "success"})
        except:
            return JsonResponse({'message': "an error ocurred"})

class LoginView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        data = json.loads(request.body)
        print(data)
        user = Usuario.objects.filter(email=data['email']).values()
        print(user)
        if len(user)>0:
            encryptPass = user[0]['password']
            decryptPass = contexto.verify(data['password'],encryptPass)
            if decryptPass==True:
                payload= {
                    "id": user[0]['id'],
                    "role_id": user[0]['role_id'],
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=120)
                }
                token = jwt.encode(payload, "secret_key", algorithm="HS256")
                info={"message":"succes", "data":{ "token": token, "id": user[0]['id'], "role_id": user[0]['role_id']}}
            else:
                info={"message":"email or password are incorrect, please try again!"}
        else:
            info={"message":"email or password are incorrect, please try again!"}
            
        return JsonResponse(info)

class UsersView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    @tokenValidate
    def get(self, request, id=0):
        if id>0:
            user = list(Usuario.objects.filter(id=id).values())
            data = {"message":"succes","data":user}
            return JsonResponse(data)
        else:
            users = list(Usuario.objects.values())
            data = {"message":"succes","data":users}
            return JsonResponse(data)

    @isAdmin
    @tokenValidate
    def post(self, request):
        data = json.loads(request.body)

        encryptPass =contexto.hash(data['password'])
        try:
            Usuario.objects.create(nombres=data['nombres'], apellidos=data['apellidos'], dni=data['dni'], tipo_dni=data['tipo_dni'], email=data['email'], password=encryptPass, hobbies=data['hobbies'], role_id=data['role_id'])
            return JsonResponse({'message': "usuario successfully created"})
        except:
            return JsonResponse({'message': "an error ocurred"})

    @tokenValidate
    def put(self, request, id):
        data = json.loads(request.body) 
        user = list(Usuario.objects.filter(id=id).values())
        encrypter = contexto.hash(data['password'])

        if len(user)>0:
            Usuario.objects.filter(id=id).values().update(nombres=data['nombres'], apellidos=data['apellidos'], dni=data['dni'], tipo_dni=data['tipo_dni'], email=data['email'], password=encrypter, hobbies=data['hobbies'], role_id='2')
            info = {'message': "usuario succesfully updated"}
        else:
            info = {'message': "Doesn't exist any user with that id"}
        return JsonResponse(info)
    
    @isAdmin
    @tokenValidate
    def delete(self, request, id):
        user = list(Usuario.objects.filter(id=id).values())
        if len(user)>0:
            Usuario.objects.filter(id=id).delete()
            info = {'message': "usuario succesfully deleted"}
        else:
            info = {'message': "Doesn't exist any user with that id"}
        return JsonResponse(info)

class RolesView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    @isAdmin
    @tokenValidate
    def get(self, request, id=0):
        if id>0:
            role = list(Roles.objects.filter(id=id).values())
            
            data = {"message":"succes","data":role}
            return JsonResponse(data)
        else:
            roles = list(Roles.objects.values())
            data = {"message":"succes","data":roles}
            return JsonResponse(data)

    @isAdmin
    @tokenValidate
    def post(self, request):
        data = json.loads(request.body)
        Roles.objects.create(nombre=data['nombre'])
        return JsonResponse({'message': "success"})

    @isAdmin
    @tokenValidate
    def put(self, request, id):
        data = json.loads(request.body)
        role = Roles.objects.filter(id=id)
        if(len(role)>0):
            Roles.objects.filter(id=id).values().update(nombre=data['nombre'])
            info={'message': "role successfully updated"}
        else:
            info={"message":"Doesn't exist any role with that id"}
        return JsonResponse(info)

    @isAdmin
    @tokenValidate
    def delete(self, request, id):
        role = list(Roles.objects.filter(id=id).values())
        if len(role)>0:
            Roles.objects.filter(id=id).delete()
            info = {'message': "role succesfully deleted"}
        else:
            info = {'message': "Doesn't exist any role with that id"}
        return JsonResponse(info)