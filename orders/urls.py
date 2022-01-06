from django.urls import path

from orders.views import OrderTransactionView
urlpatterns = [
    path('', OrderTransactionView.as_view())
]
