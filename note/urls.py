
from django.contrib import admin
from django.urls import path, include

from noteApp.views import UserLoginView, RegisterView, CustomLogoutView, HomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', UserLoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('home/', HomeView.as_view(), name='home'),
    # Google oauth 2.0
    path("", include("allauth.urls"))

]
