import datetime

from django.http  import JsonResponse
from django.views import View

from dr_martens.checkitem   import CheckItem
from django.db.models       import Max, Q

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
                "price"      : int(price),
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
            min_price   = request.GET.get("min_price", 10000)
            max_price   = request.GET.get("max_price", 500000)
            colors      = request.GET.get("colors", None)
            sizes       = request.GET.get("sizes", None)
            sort        = request.GET.get("sort", "id")
            limit       = int(request.GET.get("limit",8))
            offset      = int(request.GET.get("offset",0))

            q  = Q(productoption__stock__gt=0)
            q &= Q(productoption__price__gte=min_price)
            q &= Q(productoption__price__lte=max_price)

            if(category):
                q &= Q(productoption__subcategory__category__name=category)

            if(subcategory):
                q &= Q(productoption__subcategory__name=subcategory)

            if(colors):
                colors = colors.split(",")
                q     &= Q(productoption__color__color__in=colors)

            if(sizes):
                sizes = sizes.split(",")
                q    &= Q(productoption__size__name__in=sizes) 

            sort_set = {
                "id"       : "id",
                "price"    : "max_price",
                "-price"   : "-max_price",
                "launch"   : "-launched_at"
            }

            products = Product.objects\
                              .annotate(max_price=Max('productoption__price'))\
                              .filter(q)\
                              .order_by(sort_set[sort])

            data = [{
                    "productName"    : product.korean_name,
                    "price"          : int(product.max_price),
                    "centerColor"    : product.productoption_set.first().color.color,
                    "thumbnailImage" : product.thumbnail_image,
                    "id"             : product.id
                }for product in products[offset:offset+limit]]
            
            return JsonResponse({"result":data}, status=200)

        except ValueError as e:
            return JsonResponse({"message":"limit or offset is not number"}, status=404)
