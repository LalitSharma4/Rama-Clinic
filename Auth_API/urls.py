from django.urls import include, path
from .views import *

urlpatterns = [

    path('register', UserRegisterAPI.as_view(), name='user-register'),
    path("update/<int:user_id>", UpdateProfileAPI.as_view()),
    path("check-mobile", CheckMobileAPI.as_view()),
    path("users", GetUserAPI.as_view()),
   
    
]