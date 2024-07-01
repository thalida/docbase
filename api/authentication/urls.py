from django.urls import include, re_path
from rest_framework import routers

from .views import UserViewSet
# from .views import UserViewSet, MyUserViewSet

router = routers.SimpleRouter()
router.register(r"users", UserViewSet, basename="users")
# router.register(r"users/me", MyUserViewSet, basename="my_user")

urlpatterns = [
    re_path(r"^", include(router.urls)),
]
