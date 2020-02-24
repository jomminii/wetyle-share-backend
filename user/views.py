import json
import requests
import bcrypt
import jwt

from my_settings import SECRET_KEY
from .models import User

from django.views import View
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if User.objects.filter(login_id = data['login_id']).exists():
                return JsonResponse({"message": "existing login_id"}, status = 400)

            if len(data['password']) < 7:
                return JsonResponse({"message": "too short password"}, status = 400)

            password_crypt = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

            validate_email(data['email'])

            if User.objects.filter(email = data['email']).exists():
                return JsonResponse({"message": "existing email"}, status = 400)

            User(
                login_id = data['login_id'],
                password = password_crypt.decode('utf-8'),
                nickname  = data['nickname'],
                email     = data['email'],
                birthday  = data.get('birthday', None),
                gender    = data['gender'],
                image_url = data.get('image_url',None),
            ).save()

            token = jwt.encode({'login_id' : data['login_id']}, SECRET_KEY, algorithm = 'HS256')

            return JsonResponse({"token" : token.decode('utf-8')}, status = 200)

        except ValidationError:
            return JsonResponse({"message":"INVALID_EMAIL"}, status=400)

        except KeyError:
            return JsonResponse({"message": "INVALID_KEYS"}, status = 400)
