from django.urls import path

from products.views import DetailView, ListView

urlpatterns = [
    path('product/<int:product_id>', DetailView.as_view()),
    path('products', ListView.as_view()),
]
