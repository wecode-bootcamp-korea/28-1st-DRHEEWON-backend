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
            min_price   = request.GET.get("min_price", None)
            max_price   = request.GET.get("max_price", None)
            colors      = request.GET.get("colors", None)
            sizes       = request.GET.get("sizes", None)
            order       = request.GET.get("order", None)
            limit       = int(request.GET.get("limit",8))
            offset      = int(request.GET.get("offset",0))

            query_string = Q(stock__gt=0)
            if(min_price):
                query_string &= Q(price__gte=min_price)
            if(max_price):
                query_string &= Q(price__lte=max_price)
            if(category):
                query_string &= Q(subcategory__category__name=category)
            if(subcategory):
                query_string &= Q(subcategory__name=subcategory)

            if(colors):
                colors=colors.split(",")
                local_query_string=Q()
                for color in colors:
                    local_query_string |= Q(color__color=color) 
                query_string &= (local_query_string)

            if(sizes):
                sizes=sizes.split(",")
                local_query_string=Q()
                for size in sizes:
                    local_query_string |= Q(size__name=size)
                query_string &= (local_query_string)

            product_options = ProductOption.objects.filter(query_string)
            if order: 
                if "launch" in order:
                   order = "-product__launched_at"
                product_options = product_options.order_by(order)
 
            result           = []
            duplication_list = []
            count            = offset
            for product_option in product_options:
                korean_name     = product_option.product.korean_name
                price           = product_option.price
                color           = product_option.color.color
                thumbnail_image = product_option.product.thumbnail_image
                product_id      = product_option.product.id

                if not [product_id, color] in duplication_list:
                    duplication_list.append([product_id, color])
                    result.append(
                        {
                            "koreanName"    : korean_name,
                            "price"         : price,
                            "color"         : color,
                            "thumbnailImage": thumbnail_image,
                            "id"            : product_id
                        }
                    )
                    count += 1
                    if count >= limit+offset:
                        break

            return JsonResponse({"result":result}, status=200)

        except ValueError as e:
            return JsonResponse({"message":"limit or offset is not number"}, status=404)
