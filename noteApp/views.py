from django.shortcuts import render

from django.views.generic import TemplateView, ListView, View

from django.shortcuts import redirect

from .forms import LoginForm, RegistrationForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages


from django.utils.decorators import method_decorator


# Create your views here.

class UserLoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid credentials')
        return render(request, 'login.html', {'form': form})

class RegisterView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successful registration. Please log in.')
            return redirect('login')
        else:
            return render(request, 'register.html', {'form': form})


@method_decorator(login_required(login_url='login'), name='dispatch')
class HomeView(TemplateView):
    template_name = 'home.html'

class CustomLogoutView(View):
    def post(self, request):
        logout(request)
        return redirect('login')