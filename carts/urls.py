from django.urls import path

from carts.views import ProductCartView

urlpatterns = [
    path('', ProductCartView.as_view()),
]
