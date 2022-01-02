import jwt

from django.conf import settings

from users.models import User

SECRET_KEY = settings.SECRET_KEY
ALGORITHM  = settings.ALGORITHM


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip

def login_check(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get("Authorization", None)

            if access_token:
                payload      = jwt.decode(access_token, SECRET_KEY, algorithms=ALGORITHM)
                user         = User.objects.get(id=payload.get('id'))
                request.user = user
            else:
                request.user      = None
                request.client_ip = get_client_ip(request)

            return func(self, request, *args, **kwargs)

        except jwt.ExpiredSignatureError:
            return JsonResponse({'message':'TOKEN_EXPIRED'}, status=400)

        except User.DoesNotExist:
            return JsonResponse({'message':'UserDoesNotExist'}, status=400)

    return wrapper

