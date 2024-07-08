from django_filters import rest_framework as filters

from .models import WorkspaceInvitation


class WorkspaceInvitationFilter(filters.FilterSet):
    class Meta:
        model = WorkspaceInvitation
        fields = ["workspace", "email"]
