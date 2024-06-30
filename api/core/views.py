# Create your views here.
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins, permissions, viewsets

from docs.tags import SchemaTags

from .models import Database, Page, View, Field
from .serializers import DatabaseSerializer, PageSerializer, ViewSerializer, FieldSerializer


@extend_schema(tags=[SchemaTags.CORE__DATABASE.value])
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


@extend_schema(tags=[SchemaTags.CORE__VIEW.value])
@extend_schema_view(
    list=extend_schema(summary="List Views"),
    create=extend_schema(summary="Create View"),
    retrieve=extend_schema(summary="Retrieve View"),
    update=extend_schema(summary="Update View"),
    partial_update=extend_schema(summary="Partial Update View"),
    destroy=extend_schema(summary="Delete View"),
)
class ViewViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = View.objects.all()
    serializer_class = ViewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(database__workspace__members=self.request.user)


@extend_schema(tags=[SchemaTags.CORE__PAGE.value])
@extend_schema_view(
    list=extend_schema(summary="List Pages"),
    create=extend_schema(summary="Create Page"),
    retrieve=extend_schema(summary="Retrieve Page"),
    update=extend_schema(summary="Update Page"),
    partial_update=extend_schema(summary="Partial Update Page"),
    destroy=extend_schema(summary="Delete Page"),
)
class PageViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(database__workspace__members=self.request.user)


@extend_schema(tags=[SchemaTags.CORE__FIELD.value])
@extend_schema_view(
    list=extend_schema(summary="List Fields"),
    create=extend_schema(summary="Create Field"),
    retrieve=extend_schema(summary="Retrieve Field"),
    update=extend_schema(summary="Update Field"),
    partial_update=extend_schema(summary="Partial Update Field"),
    destroy=extend_schema(summary="Delete Field"),
)
class FieldViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(database__workspace__members=self.request.user)
