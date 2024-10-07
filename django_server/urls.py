"""
URL configuration for django_server project.

The `urlpatterns` list urls URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/shop/', include('apps.product_app.url')),
    path('api/v1/debt/', include('apps.debt_app.url')),  # Import your urls
    path('api/v1/currency/', include('apps.currency_app.url')),
    path('api/v1/user/', include('apps.user_app.url')),
    path('api/v1/builder/', include('apps.builder_app.url')),
    path('api/v1/provider/', include('apps.provider_app.url')),
    path('api/v1/statistics/', include('apps.statistic_app.url')),
    path('api/v1/spiska/', include('apps.spiska_app.url')),
]
