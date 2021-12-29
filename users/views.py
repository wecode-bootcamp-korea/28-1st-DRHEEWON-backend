import json
import datetime

import jwt
import bcrypt

from django.shortcuts import render
from django.views     import View

from dr_martens.checkitem import CheckItem

class SignInView(View):

    def post(self, request):
        try:
            data = json.loads(request.body)
            signin_key_list=["user_id", "password"]
            CheckItem.check_keys_in_body(data, signin_key)
        except:
            pass
