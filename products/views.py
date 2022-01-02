import datetime

from django.http  import JsonResponse
from django.views import View

from dr_martens.checkitem   import CheckItem
from dr_martens.login_check import login_check
from django.db.models       import Q

from products.models        import (Product,
                                    ProductImage,
                                    ProductOption)

class ProductDetailView(View):
    def get(self, request, *args, **kwargs):
        try:
            product           = Product.objects.get(id=kwargs["product_id"])
            product_name      = product.korean_name
            product_id        = product.id
            material          = product.material
            country_of_origin = product.country_of_origin

            product_options   = product.productoption_set.all()
            product_images    = product.productimage_set.all()
            price             = product_options[0].price
    
            color_query_set = product_options.values_list("color__color").distinct()
            colors          = [color for color in color_query_set]

            sizes_stocks = [
                {
                    "size"    : product_option.size.name,
                    "quantity": product_option.stock
                }for product_option in product_options
            ]
             
            img_urls = [product_image.url for product_image in product_images]

            result = {
                "id"         : product_id,
                "productName": product_name,
                "imageUrls"  : img_urls,
                "country"    : country_of_origin,
                "material"   : material,
                "centerSize" : sizes_stocks,
                "centerColor": colors,
                "price"      : price,
            }
            
            return JsonResponse({"result":result}, status=200)

        except KeyError as e:
            return JsonResponse({"message":getattr(e,"message",str(e))},status=400)

        except Product.DoesNotExist:
            return JsonResponse({"message":"Product does not found"}, status=404)

class ListView(View):
    def get(self, request, *args, **kwargs):

        min_price = request.GET.get("min_price", None)
        max_price = request.GET.get("max_price", None)
        colors    = request.GET.get("colors", None)
        sizes     = request.GET.get("sizes", None)
        order     = request.GET.get("order", None)
        print(type(order))
        query_string = Q(stock__gt=0)
        if(min_price):
            query_string &= Q(price__gte=min_price)
        if(max_price):
            query_string &= Q(price__lte=max_price)
        if(colors):
            query_string &= Q(color__color__in=colors.split("."))
        if(sizes):
            query_string &= Q(size__name__in=sizes.split(","))

        products = ProductOption.objects.filter(query_string)

        if order: 
            if "launch" in order:
                order = "-product__launched_at"
            products = products.order_by(order)

        for i in products:
            print(i.product.korean_name, i.size.name, i.color.color, i.price, i.stock, i.product.launched_at)
        return JsonResponse({"message":"success"}, status=200)
