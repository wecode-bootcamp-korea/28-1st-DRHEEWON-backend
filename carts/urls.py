from django.urls import path

from carts.views import (CartListView,
                         CartAddView, 
                         CartChangeView,
                         CartDeleteView)

urlpatterns = [
    path('', CartListView.as_view()),
    path('/add', CartAddView.as_view()),
    path('/<int:cart_id>', CartChangeView.as_view()),
    path('/delete', CartDeleteView.as_view()),
]
