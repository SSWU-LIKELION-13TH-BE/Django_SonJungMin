from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from mypage.forms import UserUpdateForm  # 필요 시
from django.contrib.admin.sites import NotRegistered

try:
    admin.site.unregister(CustomUser)
except NotRegistered:
    pass

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    form = UserUpdateForm

    # 비밀번호 관련 필드 제거
    fieldsets = (
        (None, {'fields': ('username', 'email', 'nickname')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'nickname', 'password1', 'password2'),
        }),
    )
    
    
    list_display = ('username', 'email', 'nickname')
    search_fields = ('email', 'username')
    

admin.site.register(CustomUser, CustomUserAdmin)