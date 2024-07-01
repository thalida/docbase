from datetime import datetime

from django.utils.timezone import make_aware


def update_user(backend, strategy, details, response, user=None, *args, **kwargs):
    if backend.name == "google-oauth2":
        if response.get("picture", None) is not None:
            user.avatar = response.get("picture")

    user.last_login = make_aware(datetime.now())
    user.save()
