from django.shortcuts import render
from django.views.generic import CreateView
from social_django.models import UserSocialAuth, UserSocialAuthManager
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import requests
from django.contrib.auth import logout as auth_logout


# Create your views here.


def home(request):
    if request.user.is_authenticated:
        social = request.user.social_auth.get(provider='vk-oauth2')
        token = social.extra_data['access_token']
        api_get_friends = 'https://api.vk.com/method/friends.get'
        params = {
            'order': 'hints',
            'count': 5,
            'fields': ['city', 'country'],
            'v': 5.21,
            'access_token': token,
        }
        res = requests.get(api_get_friends, params=params)
        data = res.json()
        # print(data)
        return render(request, 'landing.html', {'data': data['response']['items']})
    else:
        return render(request, 'landing.html')


def logout(request):
    """Logs out user"""
    auth_logout(request)
    return render(request, 'landing.html')
