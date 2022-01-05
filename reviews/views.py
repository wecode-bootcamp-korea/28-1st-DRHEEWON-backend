import datetime

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Avg, Sum, Count

from reviews.models import Review

class ReviewListView(View):
    def get(self, request, *args, **kwargs):
        try:
            product_id = kwargs["product_id"]
            reviews = Review.objects.filter(product_id=product_id)

            today = datetime.date.today()
            base_year_for_gen = [
                datetime.datetime(today.year-(i*10+9),1,1)
                for i in range(1,5)
            ]
            base_year_for_gen.insert(0,today)
            base_year_for_gen.append(datetime.datetime(1900,1,1))

            num_people_generation = []
            print(reviews.filter(user__birthday__range=(base_year_for_gen[1],base_year_for_gen[0])).count())
            #for i in range(len(base_year_for_gen)-1):
                #num_people_generation.append(reviews.filter(user__birthday__range=(base_year_for_gen[i],base_year_for_gen[i+1])).count())
            
            print(num_people_generation)

            print(base_year_for_gen)
            #avg_star = reviews.aggregate(avg_star=Avg('star_point'))
            #print(avg_star['avg_star'])
            
            return JsonResponse({"result":"result"}, status=200) 
        except KeyError:
            return JsonResponse({"message":"KeyError"}, status=401)

