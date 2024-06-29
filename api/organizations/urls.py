from django.urls import include, re_path
from rest_framework import routers

from .views import WorkspaceViewSet

router = routers.SimpleRouter()

router.register(r"workspaces", WorkspaceViewSet, basename="users")

urlpatterns = [
    re_path(r"^", include(router.urls)),
]
