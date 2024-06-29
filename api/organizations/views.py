from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins, permissions, viewsets

from .models import Workspace
from .serializers import WorkspaceSerializer


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
