from typing import Any

from django.contrib.auth.backends import ModelBackend, UserModel
from django.http.request import HttpRequest

from accounts.models import User


class CustomBackend(ModelBackend):
    @classmethod
    def authenticate(
        cls,
        request: HttpRequest | None = None,
        username: str = None,
        password: str = None,
        **kwargs: Any,
    ) -> User | None:
        try:
            user = UserModel.objects.filter(email=username)
        except UserModel.DoesNotExist:
            return None

        if user.exists():
            my_user = user.first()
            if my_user.check_password(password):
                return my_user
        return None
