import json
import uuid

from django.http  import JsonResponse
from django.views import View

from utils.login_required import login_required
from orders.models        import (OrderStatus,
                                  OrderItem,
                                  Order)

class ProductOrderView(View):
    @login_required
    def post(self, request, *args, **kwargs):
        try:
            user = request.user
             


            return JsonResponse({"message":"success"}, status=200)
        except KeyError as e:
            return JsonResponse({"message":getattr(e,'message',str(e))}, status=401)
