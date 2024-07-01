from django.urls import include, re_path
from rest_framework import routers

from .views import UserViewSet

router = routers.SimpleRouter()
router.register(r"users", UserViewSet, basename="users")

urlpatterns = [
    re_path(r"^", include(router.urls)),
]
