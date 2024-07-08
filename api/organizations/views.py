from django.core.exceptions import ValidationError
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

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
        return self.queryset.filter(
            Q(workspace__members=self.request.user) | Q(email=self.request.user.email)
        ).distinct()

    @action(detail=True, methods=["post"], url_path="accept")
    def accept(self, request, pk=None):
        invitation = self.get_object()

        try:
            invitation.accept(request.user)
        except ValidationError as e:
            return Response(e.message_dict, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(invitation)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="reject")
    def reject(self, request, pk=None):
        invitation = self.get_object()
        invitation.reject(request.user)

        serializer = self.get_serializer(invitation)
        return Response(serializer.data, status=status.HTTP_200_OK)
