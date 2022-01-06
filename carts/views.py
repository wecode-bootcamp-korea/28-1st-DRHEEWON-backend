import json

from django.http          import JsonResponse
from django.views         import View

from utils.login_required import login_required
from dr_martens.checkitem import CheckItem
from carts.models         import Cart
from products.models      import (ProductOption,
                                  Product,
                                  Size)

class ProductCartView(View):
    @login_required
    def get(self, request, *args, **kwargs):
        try:
            user = request.user
            
            carts = Cart.objects.filter(user=user)
            
            result = [{
                "thumbnailImage": cart.product_option.product.thumbnail_image,
                "productName"   : cart.product_option.product.korean_name,
                "centeColor"    : cart.product_option.color.color,
                "size"          : cart.product_option.size.name,
                "price"         : int(cart.product_option.price),
                "quantity"      : cart.quantity,
                "id"            : cart.id,
                "isChecked"     : False
                }for cart in carts]

            return JsonResponse({"result":result}, status=200)

        except KeyError as e:
            return JsonResponse({"message":"KeyError"}, status=401)

    @login_required
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            user = request.user

            required_keys = ["product_id", "quantity", "size", ]
            CheckItem.check_keys_in_body(data, required_keys)

            product_id  = data.get("product_id")
            quantity    = int(data.get("quantity"))
            size        = data.get("size")
            category    = data.get("category", "남자")

            product_option = ProductOption.objects.get(
                product_id                  =product_id,
                size__name                  =size,
                subcategory__category__name = category
            )
            if product_option.stock < quantity:
                return(JsonResponse({"message":"InsufficientQuantity"}, status=400))

            cart, created = Cart.objects.get_or_create(
                    user          =user, 
                    product_option=product_option,
            )
            if created:
                cart.quantity = quantity
            else:
                cart.quantity += quantity
            cart.save()

            return JsonResponse({"message":"success"}, status=201)
        except KeyError as e:
            return JsonResponse({"message":"KeyError"}, status=401)

    @login_required
    def patch(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            user = request.user 

            required_keys = ["quantity", "cart_id"]
            CheckItem.check_keys_in_body(data, required_keys)

            cart_id  = data["cart_id"]
            quantity = int(data["quantity"])

            cart = Cart.objects.get(id=cart_id)

            if cart.product_option.stock < quantity:
                return(JsonResponse({"message":"InsufficientQuantity"}, status=400))

            cart.quantity = quantity
            cart.save()

            return JsonResponse({"message":"success"}, status=201)

        except KeyError as e:
            return JsonResponse({"message":"KeyError"}, status=401)

        except Cart.DoesNotExist as e:
            return JsonResponse({"message":"CartItemDoesNotExist"}, status=404)

    @login_required
    def delete(self, request, *args, **kwargs):
        try: 
            data = json.loads(request.body)
            user = request.user

            required_keys = ["cart_id"]
            CheckItem.check_keys_in_body(data, required_keys)

            cart_id = data["cart_id"]
            Cart.objects.filter(id__in=cart_id, user=user).delete()

            return JsonResponse({"result":"success"}, status=200)
        except KeyError as e:
            return JsonResponse({"message":"KeyError"}, status=401)
