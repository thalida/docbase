from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins, permissions, viewsets

from .models import Workspace
from .serializers import WorkspaceSerializer


@extend_schema_view(
    list=extend_schema(summary="List workspaces"),
    create=extend_schema(summary="Create workspace"),
    retrieve=extend_schema(summary="Retrieve workspace"),
    update=extend_schema(summary="Update workspace"),
    destroy=extend_schema(summary="Delete workspace"),
    partial_update=extend_schema(summary="Partial update workspace"),
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
