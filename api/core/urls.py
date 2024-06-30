from django.urls import include, re_path
from rest_framework import routers

from .views import DatabaseViewSet, ViewViewSet, PageViewSet, FieldViewSet

router = routers.SimpleRouter()

router.register(r"databases", DatabaseViewSet, basename="databases")
router.register(r"views", ViewViewSet, basename="views")
router.register(r"pages", PageViewSet, basename="pages")
router.register(r"fields", FieldViewSet, basename="fields")


urlpatterns = [
    re_path(r"^", include(router.urls)),
]
