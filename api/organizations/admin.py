from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from .models import Workspace


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
