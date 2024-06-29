from django.templatetags.static import static
from django.urls import reverse_lazy
from dotenv import load_dotenv


def admin_reverse_lazy(viewname, *args, **kwargs):
    admin_urls_namespace = "team_thalida_admin"
    return reverse_lazy(f"{admin_urls_namespace}:{viewname}", args=args, kwargs=kwargs)


load_dotenv()


TEAM_THALIDA_UNFOLD = {
    "SITE_TITLE": "Team Thalida",
    "SITE_HEADER": "Team Thalida",
    "SHOW_VIEW_ON_SITE": False,
    "LOGIN": {
        "redirect_after": lambda r: admin_reverse_lazy("index"),
    },
    "STYLES": [
        lambda request: static("css/admin-styles.css"),
    ],
    "SCRIPTS": [],
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        # "navigation": [
        #     {
        #         "title": _("Navigation"),
        #         "separator": False,
        #         "items": [
        #             {
        #                 "title": _("Dashboard"),
        #                 "icon": "dashboard",
        #                 "link": reverse_lazy("admin:index"),
        #             },
        #         ],
        #     },
        #     {
        #         "title": _("Organizations"),
        #         "separator": False,
        #         "items": [
        #             {
        #                 "title": _("Workspaces"),
        #                 "icon": "workspaces",
        #                 "link": reverse_lazy("admin:organizations_workspace_changelist"),
        #             },
        #             {
        #                 "title": _("Users"),
        #                 "icon": "person",
        #                 "link": reverse_lazy("admin:authentication_user_changelist"),
        #             },
        #             {
        #                 "title": _("Groups"),
        #                 "icon": "admin_panel_settings",
        #                 "link": reverse_lazy("admin:auth_group_changelist"),
        #             },
        #         ],
        #     },
        #     {
        #         "title": _("Core"),
        #         "separator": False,
        #         "items": [
        #             {
        #                 "title": _("Databases"),
        #                 "icon": "table",
        #                 "link": reverse_lazy("admin:core_database_changelist"),
        #             },
        #             {
        #                 "title": _("Fields"),
        #                 "icon": "variable_add",
        #                 "link": reverse_lazy("admin:core_field_changelist"),
        #             },
        #             {
        #                 "title": _("Field Configs"),
        #                 "icon": "page_info",
        #                 "link": reverse_lazy("admin:core_booleanfieldconfig_changelist"),
        #             },
        #             {
        #                 "title": _("Pages"),
        #                 "icon": "description",
        #                 "link": reverse_lazy("admin:core_page_changelist"),
        #             },
        #             {
        #                 "title": _("Folders"),
        #                 "icon": "folder",
        #                 "link": reverse_lazy("admin:core_folder_changelist"),
        #             },
        #             {
        #                 "title": _("Views"),
        #                 "icon": "frame_inspect",
        #                 "link": reverse_lazy("admin:core_view_changelist"),
        #             },
        #         ],
        #     },
        # ],
    },
    # "TABS": [
    #     {
    #         "models": [
    #             "authentication.user",
    #             "social_django.usersocialauth",
    #         ],
    #         "items": [
    #             {
    #                 "title": _("All Users"),
    #                 "link": reverse_lazy("admin:authentication_user_changelist"),
    #             },
    #             {
    #                 "title": _("All Social Accounts"),
    #                 "link": reverse_lazy("admin:social_django_usersocialauth_changelist"),
    #             },
    #         ],
    #     },
    #     {
    #         "models": [
    #             "core.booleanfieldconfig",
    #             "core.checklistfieldconfig",
    #             "core.choicefieldconfig",
    #             "core.datefieldconfig",
    #             "core.filefieldconfig",
    #             "core.numberfieldconfig",
    #             "core.relationfieldconfig",
    #             "core.textfieldconfig",
    #         ],
    #         "items": [
    #             {
    #                 "title": _("Boolean Field Configs"),
    #                 "link": reverse_lazy("admin:core_booleanfieldconfig_changelist"),
    #             },
    #             {
    #                 "title": _("Checklist Field Configs"),
    #                 "link": reverse_lazy("admin:core_checklistfieldconfig_changelist"),
    #             },
    #             {
    #                 "title": _("Choice Field Configs"),
    #                 "link": reverse_lazy("admin:core_choicefieldconfig_changelist"),
    #             },
    #             {
    #                 "title": _("Date Field Configs"),
    #                 "link": reverse_lazy("admin:core_datefieldconfig_changelist"),
    #             },
    #             {
    #                 "title": _("File Field Configs"),
    #                 "link": reverse_lazy("admin:core_filefieldconfig_changelist"),
    #             },
    #             {
    #                 "title": _("Number Field Configs"),
    #                 "link": reverse_lazy("admin:core_numberfieldconfig_changelist"),
    #             },
    #             {
    #                 "title": _("Relation Field Configs"),
    #                 "link": reverse_lazy("admin:core_relationfieldconfig_changelist"),
    #             },
    #             {
    #                 "title": _("Text Field Configs"),
    #                 "link": reverse_lazy("admin:core_textfieldconfig_changelist"),
    #             },
    #         ],
    #     },
    # ],
}
