
from django.urls import path
from . import views

urlpatterns=[
    path('refresh_token',views.RegisterAPI.as_view()),
    path('access_token',views.LoginAPI.as_view())
]

