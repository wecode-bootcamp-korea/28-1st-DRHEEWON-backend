from django.urls import path

from reviews.views import ReviewListView

urlpatterns = [
    path('/<int:product_id>', ReviewListView.as_view()),
]
