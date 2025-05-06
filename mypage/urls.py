from django.urls import path
from .views import mypage_view, update_profile_view, change_password_view

app_name = 'mypage'

urlpatterns = [
    path('mypage/', mypage_view, name="mypage"),
    path('mypage/update_profile/', update_profile_view, name="update_profile"),
    path('mypage/change-password/', change_password_view, name='change_password'),
]