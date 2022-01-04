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

class ProductListView(View):
    def get(self, request, *args, **kwargs):
        try:
            category    = request.GET.get("category", None)
            subcategory = request.GET.get("subcatagory",None)
            min_price   = request.GET.get("min_price", 0)
            max_price   = request.GET.get("max_price", None)
            colors      = request.GET.getlist("color", None) #[red, blue], ?color=red&color=blue
            sizes       = request.GET.get("sizes", None)
            sort        = request.GET.get("order", "id") #sort
            limit       = int(request.GET.get("limit",8))
            offset      = int(request.GET.get("offset",0))

            q = Q(stock__gt=0)
            
            if(min_price):
                query_string &= Q(price__gte=min_price)
            
            if(max_price):
                query_string &= Q(price__lte=max_price)
            
            if(category):
                query_string &= Q(subcategory__category__name=category)
            
            if(subcategory):
                query_string &= Q(subcategory__name=subcategory)

            if(colors):
                colors = colors.split(",")  
                query_string &= Q(productoption__color__color__in=colors)

            if(sizes):
                sizes=sizes.split(",")
                query_string &= Q(productoption__size__name__in=sizes)
            
            sort_set = {
                "id"       : "id",
                "price"    : "price",
                "-price"   : "-price",
                "launched" : "-launched_at"
            }
            
            products = Product.objects\
                              .annotate(max_price=Max('productoption__price'))\
                              .filter(query_string)\
                              .order_by(sort_set[sort])

            data      = {
                "max_count" : products.count(),
                "results"   : [{
                    "korean_name"     : product.korean_name,
                    "price"           : product.max_price,
                    "color"           : [option.color.color for option in product.productoption_set.all()],
                    "thumbnail_image" : product.thumbnail_image,
                    "product_id"      : product.id
                }for product in products[offset:offset+limit]]
            }
            
            return JsonResponse({"data":data}, status=200)

        except ValueError as e:
            return JsonResponse({"message":"limit or offset is not number"}, status=404)