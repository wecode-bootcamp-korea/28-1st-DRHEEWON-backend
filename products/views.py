import datetime

from django.http  import JsonResponse
from django.views import View

from dr_martens.checkitem   import CheckItem
from dr_martens.login_check import login_check
from products.models        import (Product,
                                    ProductImage,
                                    ProductOption)

class DetailView(View):
    @login_check
    def get(self, request, *args, **kwargs):
        try:
            product           = Product.objects.get(id=kwargs["product_id"])
            product_name      = product.korean_name
            product_id        = product.id
            material          = product.material
            country_of_origin = product.country_of_origin

            product_images    = ProductImage.objects.filter(product=product)
            product_options   = ProductOption.objects.filter(product=product)
            
            price = product_options[0].price
    
            colors = []
            sizes_stocks = []
            for product_option in product_options:
                colors.append(product_option.color.color)
                sizes_stocks.append(
                    {
                        "size":product_option.size.name,
                        "quantity":product_option.stock
                    }        
                )

            colors = list(set(colors))
             
            img_urls = []
            for product_image in product_images:
                img_urls.append(product_image.url)

            result = {
                "result":{
                    "id":product_id,
                    "productName": product_name,
                    "imageUrls": img_urls,
                    "country": country_of_origin,
                    "material": material,
                    "centerSize": sizes_stocks,
                    "centerColor": colors,
                    "price": price,
                }
            }
            return JsonResponse({"message":"success","result":result}, status=200)

        except KeyError as e:
            return JsonResponse({"message":getattr(e,"message",str(e))},status=400)

        except Product.DoesNotExist:
            return JsonResponse({"message":"Product does not found"}, status=404)
