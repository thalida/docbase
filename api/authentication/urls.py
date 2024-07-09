from django.urls import include, re_path
from rest_framework import routers

from .views import UserViewSet, get_ably_token

router = routers.SimpleRouter()
router.register(r"users", UserViewSet, basename="users")

urlpatterns = [
    re_path(r"^", include(router.urls)),
    re_path(r"^auth/ably-token/", get_ably_token, name="get_ably_token"),
]
