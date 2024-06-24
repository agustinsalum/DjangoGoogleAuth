from django.shortcuts import render, redirect

from django.views.generic import TemplateView, ListView, View

from .forms import LoginForm, RegistrationForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.utils.decorators import method_decorator

from .models import UserProfile

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
class HomeView(ListView):
    model = UserProfile
    template_name = 'home.html'
    context_object_name = 'user_profiles'
    paginate_by = 4

    # Added the get method to handle out-of-range numbers or other issues
    def get(self, request, *args, **kwargs):
        user_profiles = self.get_queryset()
        paginator = Paginator(user_profiles, self.paginate_by)
        page_number = request.GET.get('page', 1)

        try:
            page_obj = paginator.get_page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        return render(request, self.template_name, {'page_obj': page_obj})

class CustomLogoutView(View):
    def post(self, request):
        logout(request)
        return redirect('login')