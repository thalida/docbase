from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins, permissions, viewsets
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend

from docs.tags import SchemaTags
from organizations.filters import WorkspaceInvitationFilter

from .models import Workspace, WorkspaceInvitation
from .serializers import WorkspaceInvitationSerializer, WorkspaceSerializer


@extend_schema(tags=[SchemaTags.ORGANIZATIONS__WORKSPACE.value])
@extend_schema_view(
    list=extend_schema(summary="List Workspaces"),
    create=extend_schema(summary="Create Workspace"),
    retrieve=extend_schema(summary="Retrieve Workspace"),
    update=extend_schema(summary="Update Workspace"),
    partial_update=extend_schema(summary="Partial Update Workspace"),
    destroy=extend_schema(summary="Delete Workspace"),
)
class WorkspaceViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(members=self.request.user)


@extend_schema(tags=[SchemaTags.ORGANIZATIONS__WORKSPACEINVITATION.value])
@extend_schema_view(
    list=extend_schema(summary="List Workspace Invitations"),
    create=extend_schema(summary="Create Workspace Invitation"),
    retrieve=extend_schema(summary="Retrieve Workspace Invitation"),
    update=extend_schema(summary="Update Workspace Invitation"),
    partial_update=extend_schema(summary="Partial Update Workspace Invitation"),
    destroy=extend_schema(summary="Delete Workspace Invitation"),
)
class WorkspaceInvitationViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = WorkspaceInvitation.objects.all()
    serializer_class = WorkspaceInvitationSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [DjangoFilterBackend]
    filterset_class = WorkspaceInvitationFilter

    def get_queryset(self):
        return self.queryset.filter(Q(workspace__members=self.request.user) | Q(email=self.request.user.email))
