from django.urls import path
from .views import signup_view, home, login_view, logout_view, findPWwithID_view, findPWwithID_view, kakao_login_view, kakao_callback_view, naver_callback_view, naver_login_view
from django.contrib.auth import views as auth_views

app_name = 'user'

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('findpwwithid/', findPWwithID_view, name='findpwwithid'),
    # path('change-password/', auth_views.PasswordChangeView.as_view()),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('kakao/login/', kakao_login_view, name='kakao_login'),
    path('kakao/callback/', kakao_callback_view, name='kakao_callback'),
    path('naver/login/', naver_login_view, name='naver_login'),  # 네이버 로그인 URL
    path('naver/callback/', naver_callback_view, name='naver_callback'),  # 콜백 URL
    
]