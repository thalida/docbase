from django.urls import include, re_path
from rest_framework import routers

from .views import WorkspaceViewSet, WorkspaceInvitationViewSet

router = routers.SimpleRouter()

router.register(r"workspaces", WorkspaceViewSet, basename="workspaces")
router.register(r"workspace-invitations", WorkspaceInvitationViewSet, basename="workspace-invitations")

urlpatterns = [
    re_path(r"^", include(router.urls)),
]
