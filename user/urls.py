from django.urls import path
from .views import signup_view, home, login_view, logout_view, findpw_view

app_name = 'user'

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('findpw/', findpw_view, name='findpw'),
]