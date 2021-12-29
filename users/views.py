import json
import datetime

import jwt
import bcrypt

from django.http      import JsonResponse
from django.views     import View
from django.conf      import settings

from users.models         import User
from dr_martens.checkitem import CheckItem

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
