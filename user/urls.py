from user.views import SignUpView
from django.urls import path

urlpatterns = [
    path('sign-up/', SignUpView.as_view()),
]
