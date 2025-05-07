from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from post.models import Post

# Create your views here.
def mypage_view(request):
    myposts=Post.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'mypage.html', {'myposts':myposts})

@login_required
def update_profile_view(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            return redirect('mypage:mypage')
    else:
        u_form = UserUpdateForm(instance=request.user)

    return render(request, 'update_profile.html', {'u_form': u_form})

@login_required
def change_password_view(request):
    if request.method == 'POST':
        pw_form = PasswordChangeForm(user=request.user, data=request.POST)
        if pw_form.is_valid():
            pw_form.save()
            update_session_auth_hash(request, pw_form.user)  # 로그인 유지
            return redirect('mypage:mypage')
    else:
        pw_form = PasswordChangeForm(user=request.user)

    return render(request, 'change_password.html', {'pw_form': pw_form})