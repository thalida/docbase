from django.urls import include, re_path
from rest_framework import routers

from .views import DatabaseViewSet

router = routers.SimpleRouter()

router.register(r"databases", DatabaseViewSet, basename="databases")

urlpatterns = [
    re_path(r"^", include(router.urls)),
]
