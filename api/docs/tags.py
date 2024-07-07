from enum import Enum


class SchemaTags(Enum):
    AUTHENTICATION__USERS = "Users"
    CORE__DATABASE = "Databases"
    CORE__VIEW = "Views"
    CORE__PAGE = "Pages"
    CORE__FIELD = "Fields"
    ORGANIZATIONS__WORKSPACE = "Workspaces"
    ORGANIZATIONS__WORKSPACEINVITATION = "Workspace Invitations"
