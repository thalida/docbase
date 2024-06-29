from django.urls import URLResolver
from unfold.sites import UnfoldAdminSite


class AdminSite(UnfoldAdminSite):
    settings_name = "TEAM_THALIDA_UNFOLD"
    urls_namespace = "team_thalida_admin"

    @property
    def urls(self) -> tuple[list[URLResolver], str, str]:
        return self.get_urls(), self.urls_namespace, self.name  # type: ignore
