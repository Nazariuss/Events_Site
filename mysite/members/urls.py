from django.urls import path
from .views import *

urlpatterns = [
    path('login_user/', login_user, name='login_user'),
    path('logout_user/', logout_user, name='logout_user'),
    path('register_user/', register_user, name='register_user'),
]
