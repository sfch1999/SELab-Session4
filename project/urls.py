"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from seproject.views import API, Register, Login, Profile, Token
from Book.views import BookAPI

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/main', API.as_view({'post': 'handle_request'})),
    path('api/register', Register.as_view({'post': 'handle_request'})),
    path('api/login', Login.as_view({'post': 'handle_request'})),
    path('api/token', Token.as_view({'post': 'handle_request'})),
    path('api/profile', Profile.as_view({'post': 'handle_request'})),
    path('api/book', BookAPI.as_view({'post': 'handle_request'})),
]
