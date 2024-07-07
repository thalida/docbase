from django_filters import rest_framework as filters

from .models import WorkspaceInvitation


class WorkspaceInvitationFilter(filters.FilterSet):
    email = filters.CharFilter(field_name="email", lookup_expr="icontains")

    class Meta:
        model = WorkspaceInvitation
        fields = ["workspace", "email"]
