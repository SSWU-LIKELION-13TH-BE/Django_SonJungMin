from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from .models import CustomUser
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse 

def home(request):
    return render(request, 'home.html')
    
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('user:home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form':form})

def login_view(request):
    if request.method == 'POST':
        l_username=request.POST['l_username']
        l_password=request.POST['l_password']
        user=authenticate(request, username=l_username, password=l_password)
        if user is not None:
            auth.login(request, user)
            return redirect('user:home')
        return redirect('user:login')
    else:
        return render(request, 'login.html')
        
def logout_view(request):
    if request.method=="GET":
        if request.user:
            auth.logout(request)
            return redirect('user:home')
    return redirect('user:home')

def findPWwithID_view(request):
    if request.method == "POST":
        password1=request.POST['f_pw1']
        password2=request.POST['f_pw2']
        user=CustomUser.objects.get(username=request.POST['f_username'])
        if(user is not None and user.email==request.POST['f_email'] and password1==password2):
            user.password=make_password(password1)
            user.save()
        return redirect('user:home')
    else:
        return render(request, 'findPWwithID.html')


import requests
from django.http import JsonResponse
from myproject import conf

def kakao_login_view(request):
    redirect_uri = "http://127.0.0.1:8000/user/kakao/callback"
    kakao_client_id = conf.KAKAO_CLIENT_ID
    kakao_login_url= f"https://kauth.kakao.com/oauth/authorize?response_type=code&client_id={kakao_client_id}&redirect_uri={redirect_uri}"

    return redirect(kakao_login_url)

def kakao_callback_view(request):
    
    code = request.GET.get('code')  # 카카오에서 전달한 code 값을 가져옴

    if not code:
        return HttpResponse('Code not found', status=400)

    # 카카오 API에 access_token을 요청하는 코드
    kakao_token_url = 'https://kauth.kakao.com/oauth/token'
    data = {
        'grant_type': 'authorization_code',
        'client_id': conf.KAKAO_CLIENT_ID,  # 카카오 앱의 REST API 키
        'redirect_uri': conf.KAKAO_REDIRECT_URI,  # 카카오 개발자 센터에 등록된 Redirect URI
        'code': code,
    }

    response = requests.post(kakao_token_url, data=data)
    token_data = response.json()

    # print(f"Response from Kakao token API: {token_data}")   # 토큰 제대로 받고 있나 확인

    if 'access_token' not in token_data:
        return HttpResponse('Failed to get access token', status=400)

    access_token = token_data['access_token']

    # 카카오 사용자 정보 가져오기
    kakao_user_info_url = 'https://kapi.kakao.com/v2/user/me'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    user_info_response = requests.get(kakao_user_info_url, headers=headers)
    user_info = user_info_response.json()

    # print(user_info)    # 정보 제대로 받고 있나 확인

    # 사용자 정보에서 필요한 데이터 추출
    kakao_id = user_info['id']
    nickname = user_info.get('properties', {}).get('nickname', '')
    email = user_info.get('kakao_account', {}).get('email', '')

    # print(f"Kakao ID: {kakao_id}")  # kakao ID 제대로 받고 있나 확인
    # print(f"Nickname: {nickname}")  # nickname 제대로 받고 있나 확인

    if not email:   # 이메일을 받으려면 비즈 어쩌구를 신청해야함(내 생각에는 정식 개발용인 것 같음) -> 결론적으로 현재는 email을 못 받으니까 이렇게 None 값으로 넣어줌
        email = None


    # 카카오 ID로 사용자 찾기 또는 새로 생성
    user, created = CustomUser.objects.get_or_create(
        kakao_id=kakao_id,
        defaults={
            'username': nickname,  # 기본적으로 카카오에서 제공하는 닉네임을 사용자 이름으로 사용
            'nickname': nickname,
            'email' : email,   # 내 생각에는 계속 인증 오류 발생하는 게, email을 빈칸으로 둬서 그런 것 같기도 하고... 일단 이거 작성하니까 로그인 됐음
        }
    )

    # 만약 사용자가 이미 존재하면 정보 업데이트
    if not created:
        # user.username = nickname # 그런데 이렇게 하면 로그인할 때마다 username이랑 nickname이 원상복구 됨.... 그래서 일단은 주석으로 막아뒀는데, 괜찮은지는 아직 테스트 못 해봄
        # user.nickname = nickname  # 괜찮음!!!!!! 오예~~!!!!!! 
        user.save()

    login(request, user)

    return redirect('user:home')


import urllib.parse

def naver_login_view(request):
    client_id = conf.NAVER_CLIENT_ID
    redirect_uri = urllib.parse.quote(conf.NAVER_REDIRECT_URI)  # URL 인코딩
    state = 'random_state_string'  # CSRF 보호용 임의의 문자열
    auth_url = f"https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&state={state}"
    return redirect(auth_url)

def naver_callback_view(request):
    code = request.GET.get('code')
    state = request.GET.get('state')

     # 디버그용 출력
    print("네이버 인증 코드:", code)  # 인증 코드 출력
    print("상태 코드:", state)  # 상태 출력

    # 네이버 액세스 토큰 요청
    token_url = 'https://nid.naver.com/oauth2.0/token'
    client_id = conf.NAVER_CLIENT_ID
    client_secret = conf.NAVER_CLIENT_SECRET
    redirect_uri = conf.NAVER_REDIRECT_URI

    token_data = {
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'state': state,
    }

    response = requests.post(token_url, data=token_data)
    print("액세스 토큰 요청 응답:", response.json())  # 액세스 토큰 응답 출력
    token_info = response.json()

    # 액세스 토큰 얻기
    access_token = token_info.get('access_token')

    if access_token:
        print("액세스 토큰:", access_token)
    else:
        print("액세스 토큰 오류 발생:", token_info)

    # 네이버 API로 사용자 정보 요청
    user_info_url = 'https://openapi.naver.com/v1/nid/me'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    user_info_response = requests.get(user_info_url, headers=headers)

    print("사용자 정보 요청 응답:", user_info_response.json())
    user_info = user_info_response.json()

    # 사용자 정보에서 필요한 데이터 가져오기
    naver_id = user_info.get('response', {}).get('id')
    nickname = user_info.get('response', {}).get('nickname')
    email = user_info.get('response', {}).get('email')

    user, created = CustomUser.objects.get_or_create(naver_id=naver_id, defaults={'username':email, 'email': email, 'nickname': nickname})

    if not created:
        # user.username = nickname # 그런데 이렇게 하면 로그인할 때마다 username이랑 nickname이 원상복구 됨.... 그래서 일단은 주석으로 막아뒀는데, 괜찮은지는 아직 테스트 못 해봄
        # user.nickname = nickname  # 괜찮음!!!!!! 오예~~!!!!!! 
        user.save()

    login(request, user)
    # 로그인 처리 (예: 사용자 등록 및 세션 처리)
    # 여기서 필요한 로직을 추가하여 사용자를 등록하거나 세션에 로그인 상태를 저장합니다.

    return redirect('user:home')  # 로그인 후 리다이렉트