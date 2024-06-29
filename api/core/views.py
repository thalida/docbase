# Create your views here.
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins, permissions, viewsets

from .models import Database
from .serializers import DatabaseSerializer


@extend_schema_view(
    list=extend_schema(summary="List Databases"),
    create=extend_schema(summary="Create Database"),
    retrieve=extend_schema(summary="Retrieve Database"),
    update=extend_schema(summary="Update Database"),
    partial_update=extend_schema(summary="Partial Update Database"),
    destroy=extend_schema(summary="Delete Database"),
)
class DatabaseViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Database.objects.all()
    serializer_class = DatabaseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(workspace__members=self.request.user)
