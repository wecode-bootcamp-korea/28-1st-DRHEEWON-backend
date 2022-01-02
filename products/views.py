import datetime

from django.http  import JsonResponse
from django.views import View

from dr_martens.checkitem   import CheckItem
from dr_martens.login_check import login_check
from products.models        import (Product,
                                    ProductImage,
                                    ProductOption)

class ProductDetailView(View):
    @login_check
    def get(self, request, *args, **kwargs):
        try:
            product           = Product.objects.get(id=kwargs["product_id"])
            product_name      = product.korean_name
            product_id        = product.id
            material          = product.material
            country_of_origin = product.country_of_origin

            product_options   = product.productoption_set.all()
            product_images    = product.productimage_set.all()
            price = product_options[0].price
    
            colors = [
                product_option.color.color 
                for product_option in product_options
            ]
            colors = list(set(colors))

            sizes_stocks = [
                {
                    "size":product_option.size.name,
                    "quantity":product_option.stock
                }
                for product_option in product_options
            ]
             
            img_urls = [
                product_image.url
                for product_image in product_images
            ]

            result ={
                "id":product_id,
                "productName": product_name,
                "imageUrls": img_urls,
                "country": country_of_origin,
                "material": material,
                "centerSize": sizes_stocks,
                "centerColor": colors,
                "price": price,
            }
            
            return JsonResponse({"result":result}, status=200)

        except KeyError as e:
            return JsonResponse({"message":getattr(e,"message",str(e))},status=400)

        except Product.DoesNotExist:
            return JsonResponse({"message":"Product does not found"}, status=404)
