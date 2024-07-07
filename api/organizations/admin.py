from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from .models import Workspace, WorkspaceInvitation


class WorkspaceMembershipInline(TabularInline):
    model = Workspace.members.through
    extra = 0
    exclude = ("created_by", "updated_by")


@admin.register(Workspace)
class WorkspaceAdmin(ModelAdmin):
    list_display = ("name", "created_at", "updated_at")
    search_fields = ("name",)
    exclude = ("created_by", "updated_by")

    inlines = [WorkspaceMembershipInline]


@admin.register(WorkspaceInvitation)
class WorkspaceInvitationAdmin(ModelAdmin):
    list_display = ("email", "workspace", "status", "created_at", "updated_at")
    search_fields = ("email", "workspace__name")
    exclude = ("created_by", "updated_by")
    readonly_fields = ("token",)
