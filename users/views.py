import json
import datetime

from django.http.response import HttpResponse, HttpResponseRedirect

import jwt
import bcrypt

from django.http      import JsonResponse
from django.views     import View
from django.conf      import settings

from users.models         import User
from dr_martens.checkitem import CheckItem
from django.contrib import auth

class SignUpView(View):

    def post(self, request):
        try:
            data = json.loads(request.body)
            
            if User.objects.filter(user_id=data['user_id']).exists():
                return JsonResponse({'message' : 'user exists'}, status=400)

            password = data['password']     
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
            User.objects.create(
                username      = data['username'],
                user_id       = data['user_id'],
                password      = hashed_password,
                mobile_number = data['mobile_number'],
                email         = data['email'],
                point         = data['point'],
            )
            return JsonResponse({'message' : 'SUCCESS'}, status=201)
        except KeyError:
            return JsonResponse({'message' : 'KeyError'}, status=400)

class SignInView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            signin_key_list = ["user_id", "password"]
            CheckItem.check_keys_in_body(data, signin_key_list)

            user_id  = data["user_id"]
            password = data["password"].encode('utf-8')

            user = User.objects.get(user_id = user_id)
            
            valid_password = user.password.encode('utf-8')

            if not bcrypt.checkpw(password, valid_password):
                return JsonResponse({'message':'INVALID_USER'}, status=401)

            exp_date = datetime.datetime.utcnow() + datetime.timedelta(hours=2)
            access_token = jwt.encode(
                    {'id':user.id, 'exp':exp_date},
                    settings.SECRET_KEY,
                    algorithm=settings.ALGORITHM,
                    )
            return JsonResponse({'message':'success','token':access_token}, status=200)

        except KeyError as e:
            return JsonResponse({'message':getattr(e,'message',str(e))}, status=400)

        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status=401)

class LogOutView(View):
    def logout(request):
        auth.logout(request)
        return HttpResponseRedirect('home')