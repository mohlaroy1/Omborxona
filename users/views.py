from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

from django.shortcuts import render, redirect
from django.views import View

from config import settings


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('sections')
        messages.error(request, "Username va/yoki password noto'g'ri! ")
        return self.get(request)



def logout_view(request):
    logout(request)
    return redirect(settings.LOGIN_REDIRECT_URL)