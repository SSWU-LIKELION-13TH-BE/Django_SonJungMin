from django.urls import path
from .views import mypage_view, update_profile_view, change_password_view, otherpage_view, write_guestbook_view, delete_guestbook_view

app_name = 'mypage'

urlpatterns = [
    path('mypage/', mypage_view, name="mypage"),
    path('mypage/update_profile/', update_profile_view, name="update_profile"),
    path('mypage/change-password/', change_password_view, name='change_password'),
    path('otherpage/<int:user_id>/', otherpage_view, name="otherpage"),
    path('otherpage/<int:user_id>/write_guestbook/', write_guestbook_view, name="write_guestbook"),
    path('otherpage/<int:user_id>/delete_guestbook/<int:guestbook_id>/', delete_guestbook_view, name="delete_guestbook"),
]