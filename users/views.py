from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.


class RegistrationView(View):

    def get(self, request):
        form = UserCreationForm()
        return render(request, 'users/registration.html', context={'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'User {username} successfully registered!')
            return redirect('signin_url')
        else:
            return render(request, 'users/registration.html', context={'form': form})


class ProfileView(View):

    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'users/profile.html')


def validate_username(request):
    if request.GET:
        username = request.GET.get('username')
        is_taken = User.objects.filter(username=username).exists()
        if is_taken:
            data = {'is_taken': 'A user with that username already exists.'}
            return JsonResponse(data)
        else:
            data = {'is_free': 'This name is free'}
            return JsonResponse(data)
