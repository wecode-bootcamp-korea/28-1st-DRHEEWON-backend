import json
import datetime
import bcrypt
from django.http.response import HttpResponse, HttpResponseRedirect

from django.http      import JsonResponse
from django.views     import View
from users.models     import User
from users.validators import confirm_email, confirm_password

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
