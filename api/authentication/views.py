from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins, permissions, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response

from api.ably import ably_client
from authentication.filters import UserFilter
from authentication.models import User
from authentication.serializers import MyUserSerializer, UserSerializer
from docs.tags import SchemaTags


@extend_schema(tags=[SchemaTags.AUTHENTICATION__USERS.value])
@extend_schema_view(
    retrieve=extend_schema(
        summary="Retrieve user",
        responses=UserSerializer,
    ),
    list=extend_schema(summary="List users", responses=UserSerializer),
    get_me=extend_schema(
        summary="Retrieve my user",
        responses=MyUserSerializer,
    ),
    update_me=extend_schema(
        summary="Update my user",
        responses=MyUserSerializer,
    ),
    partial_update_me=extend_schema(
        summary="Partial update my user",
        responses=MyUserSerializer,
    ),
)
class UserViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilter

    def is_me(self):
        return self.kwargs.get("pk") == self.request.user.id or self.kwargs.get("pk") == "me"

    def get_object(self):
        if self.is_me():
            return self.request.user
        return super().get_object()

    def get_queryset(self):
        if self.is_me():
            return User.objects.filter(id=self.request.user.id)

        return User.objects.filter(workspaces__in=self.request.user.workspaces.all()).distinct()

    def get_serializer_class(self):
        if self.is_me():
            return MyUserSerializer
        return super().get_serializer_class()

    @action(detail=False, methods=["get"], url_path="me")
    def get_me(self, request, *args, **kwargs):
        self.kwargs["pk"] = request.user.id
        return self.retrieve(request, *args, **kwargs)

    @action(detail=False, methods=["put"], url_path="me")
    def update_me(self, request, *args, **kwargs):
        kwargs["pk"] = request.user.id
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    @action(detail=False, methods=["patch"], url_path="me")
    def partial_update_me(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update_me(request, *args, **kwargs)

    def perform_update(self, serializer):
        serializer.save()


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def get_ably_token(request):
    token_params = {
        "client_id": str(request.user.id),
        "ttl": 24 * 60 * 60,
    }
    token_details = ably_client.auth.request_token(token_params=token_params)
    return Response(token_details.to_dict())
