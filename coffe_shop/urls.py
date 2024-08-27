
from django.contrib import admin
from django.urls import path
from api.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',RegisterAPI.as_view()),
    path('verify/',VerifyOtp.as_view())
]
