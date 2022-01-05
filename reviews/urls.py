from django.urls import path

from reviews.views import (ReviewStatView,
                           ReviewListView)

urlpatterns = [
    path('/<int:product_id>/comments', ReviewListView.as_view()),
    path('/<int:product_id>', ReviewStatView.as_view()),
]
