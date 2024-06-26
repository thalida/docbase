"""
URL configuration for api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import include, path, re_path
from drf_spectacular.views import SpectacularAPIView

from docs.views import SpectacularElementsView

import authentication.urls
import organizations.urls
import core.urls

api_urls = []
api_urls.extend(authentication.urls.urlpatterns)
api_urls.extend(organizations.urls.urlpatterns)
api_urls.extend(core.urls.urlpatterns)

urlpatterns = [
    # API Docs
    path("", SpectacularElementsView.as_view(), name="docs"),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    # API
    path("api/", include(api_urls)),
    re_path(r"^api/auth/", include("drf_social_oauth2.urls", namespace="drf")),
    # Admin
    path("admin/", admin.site.urls),
] + api_urls
