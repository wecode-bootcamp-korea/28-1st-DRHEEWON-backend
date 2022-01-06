import json
import datetime
import jwt
import bcrypt

from django.http      import JsonResponse
from django.views     import View
from django.conf      import settings

from users.models         import User
from dr_martens.checkitem import CheckItem
from users.validators     import confirm_email, confirm_password

class SignInView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            required_keys = ["user_id", "password"]
            CheckItem.check_keys_in_body(data, required_keys)

            user_id  = data["user_id"]
            password = data["password"].encode('utf-8')

            user           = User.objects.get(user_id = user_id)
            valid_password = user.password.encode('utf-8')

            if not bcrypt.checkpw(password, valid_password):
                return JsonResponse({'message':'INVALID_USER','status':401}, status=401)

            exp_date     = datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            access_token = jwt.encode(
                    {'id':user.id, 'exp':exp_date},
                    settings.SECRET_KEY,
                    algorithm=settings.ALGORITHM,
            )
            message = {
                'message' : 'success',
                'status'  : 200,
                'token'   : access_token,
                'username': user.username
            }
            return JsonResponse(message, status=200)

        except KeyError as e:
            return JsonResponse({'message':getattr(e,'message',str(e))}, status=400)

        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER','status':401}, status=401)
            
class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            if not confirm_email(data['email']):
                return JsonResponse({'message' : 'impossible email'}, status=400)
            
            if not confirm_password(data['password']):
                return JsonResponse({'message' : 'impossible password'}, status=400)
            
            if User.objects.filter(user_id=data['user_id']).exists():
                return JsonResponse({'message' : 'user exists'}, status=400)

            password        = data['password']     
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

    def get(self, request, *args, **kwargs):
        try:
            user_id = resquest.GET['user-id']

            if User.objects.filter(user_id=user_id).exists():
                return JsonResponse({'message':'UserExists'}, status=400)

            return JsonResponse({'message':'UserDoesNotExists'}, status=200)
        except KeyError:
            return JsonResponse({'message':'KeyError'}, status=401)
