from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import validate_email
from django.db import models

from accounts.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = 'usuário'
        verbose_name_plural = 'usuários'

    email = models.EmailField(
        'email',
        unique=True,
        blank=False,
        validators=[validate_email],
    )

    is_staff = models.BooleanField('status de staff', default=False)
    is_superuser = models.BooleanField(
        'status de super usuário',
        default=False,
    )
    date_joined = models.DateField('data de cadastro', auto_now_add=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    REQUIRED_FIELDS = ['password']

    objects = UserManager()

    def __str__(self) -> str:
        return self.email
