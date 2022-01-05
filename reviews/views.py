import datetime
import zoneinfo

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Avg, Sum, Count
from django.utils     import timezone

from reviews.models import Review

class ReviewStatView(View):
    def get(self, request, *args, **kwargs):
        try:
            product_id = kwargs["product_id"]
            reviews = Review.objects.filter(product_id=product_id)

            today = timezone.now()
            korea_tz = zoneinfo.ZoneInfo("Asia/Seoul")
            #print(timezone.now().year)
            base_year_for_gen = [
                datetime.datetime(today.year-(i*10+9), 1, 1, tzinfo=korea_tz)
                for i in range(1,5)
            ]

            base_year_for_gen.insert(0,today)
            base_year_for_gen.append(datetime.datetime(1900,1,1, tzinfo=korea_tz))

            num_people_generation = [
                reviews\
                .filter(
                    user__birthday__range = (
                        base_year_for_gen[i+1],
                        base_year_for_gen[i]
                    )
                ).count()
            for i in range(len(base_year_for_gen)-1)]
            
            num_reviews = reviews.count()
            
            num_male   = reviews.filter(user__gender=1).count()
            num_female = reviews.filter(user__gender=2).count() 
            
            result={ 
                "generationInformation":[{
                    "id"      : i+1,
                    "age"     : str(i+1)+"0대",
                    "percent" : round(num_people_generation[i]/num_reviews*100)
                }for i in range(5)],
                "male"   : round(num_male/num_reviews*100),
                "female" : round(num_female/num_reviews*100),
            }

            return JsonResponse({"result":result}, status=200)

        except KeyError:
            return JsonResponse({"message":"KeyError"}, status=401)

class ReviewListView(View):
    def get(self, request, *args, **kwargs):
        try:
            product_id = kwargs["product_id"]
            offset     = int(request.GET.get("offset", 0))
            limit      = int(request.GET.get("limit", 3))

            reviews = Review.objects.filter(product_id=product_id).order_by("id")

            num_reviews = reviews.count()

            result = [{
                "id"         : review.id,
                "userName"   : review.user.username,
                "avatar"     : review.user.profile_image_url,
                "ratingStar" : review.star_point,
                "title"      : review.title,
                "content"    : review.comment,
                }for review in reviews[offset:offset+limit]]
            result.insert(0, num_reviews-offset)

            return JsonResponse({"result":result}, status=200)

        except KeyError:
            return JsonResponse({"message":"KeyError"}, status=401)
