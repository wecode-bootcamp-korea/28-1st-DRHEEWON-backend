from django.urls import path

from orders.views import ProductOrderView

urlpatterns = [
    path('', ProductOrderView.as_view())
]
