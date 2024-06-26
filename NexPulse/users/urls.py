from django.urls import path
from .views import *

urlpatterns = [
    path('home/<int:user_id>/', home,name='home'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('signup/', signup, name='signup'),
    path('userpost/<int:user_id>/', userpost, name='userpost')
]