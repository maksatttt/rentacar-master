"""rentacar_n URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include

from core import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'add_car/', views.add_car, name='add_car'),
    url(r'^rent_car/([^/]+)/', views.rent_car),

    # Account Urls
    url(r'^login/', views.login, name='login'),
    url(r'^logout/$', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    url(r'^my_account/', views.my_account, name='my_account'),

    # API Urls
    path('api/', include('rentacar_n.urls_api')),
    path('api-auth/', include('rest_framework.urls')),

    # ADMINS
    path('admin/', admin.site.urls),

]
