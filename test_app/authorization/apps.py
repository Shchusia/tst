from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AuthorizationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authorization'
    verbose_name = _("Authorization")

    def ready(self):
        from .models import User

        try:
            for user in User.objects.all():
                User.check_role(User, instance=user)
        except Exception:
            pass