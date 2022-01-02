from django.urls import path
from users.views import SignInView, LogOutView, SignUpView

urlpatterns = [
        path('/signup', SignUpView.as_view()),
        ]
