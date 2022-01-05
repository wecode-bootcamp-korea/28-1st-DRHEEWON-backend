import json
import uuid

from django.http  import JsonResponse
from django.views import View
from django.db    import transaction

from dr_martens.checkitem import CheckItem
from utils.login_required import login_required
from carts.models         import Cart
from orders.models        import (Order,
                                  OrderItem,
                                  OrderStatus)

class OrderTransactionView(View):
    @login_required
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            user = request.user

            required_keys = ["cart_id"]
            CheckItem.check_keys_in_body(data, required_keys)

            cart_id = data["cart_id"]

            carts = Cart.objects.filter(user=user, id__in=cart_id)
            uuid_        = uuid.uuid4() 
            order_status = OrderStatus.objects.get(status="ReadyToDeliver") 
            order        = Order.objects.create(
                user        =user, 
                order_number=uuid_,
                order_status=order_status
            )

            order_items = [
                OrderItem.objects.create(
                    product_option=cart.product_option,
                    order         =order,
                    quantity      =cart.quantity,
                )for cart in carts]
     
            carts.delete()

            return JsonResponse({"message":"success"}, status=201)

        except KeyError as e:
            return JsonResponse({"message":getattr(e, 'message', str(e))}, status=401)
