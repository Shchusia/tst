from django.db import models
from django.contrib.admin import SimpleListFilter
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _

from .permissions import get_global_manager_permissions, get_business_manager_permissions, \
    get_business_admin_permissions, get_global_admin_permissions
from business.models import Business
from django.db.models.signals import post_init, post_save, pre_delete


# Create your models here.
# class BusinessListFilter(SimpleListFilter):
class Role:
    def set_permissions(self, obj):
        self.permissions_func(obj)

    def __init__(self, name, permissions_func):
        self.name = name
        self.permissions_func = permissions_func

    def __str__(self):
        return self.name


Roles = dict(
    global_admin=Role(_("Global Admin"), get_global_admin_permissions),
    global_manager=Role(_("Global Manager"), get_global_manager_permissions),
    business_admin=Role(_("Business Admin"), get_business_admin_permissions),
    business_manager=Role(_("Business Manager"), get_business_manager_permissions),
)

ROLE_CHOICES = [
    ("global_admin", Roles["global_admin"].name),
    ("global_manager", Roles["global_manager"].name),
    ("business_admin", Roles["business_admin"].name),
    ("business_manager", Roles["business_manager"].name),
]

class UserManager(BaseUserManager):
    def create_user(
        self, email, first_name, last_name, role, password=None, business=None
    ):
        if first_name is None:
            raise TypeError(_("Users should have a first name"))
        if last_name is None:
            raise TypeError(_("Users should have a last name"))
        if email is None:
            raise TypeError(_("Users should have an Email"))

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            role=role,
            business=business,
        )
        user.is_staff = True
        user.is_active = True
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        if password is None:
            raise TypeError(_("Password should not be none"))

        user = self.create_user(email, first_name, last_name, "global_admin", password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        max_length=255, unique=True, db_index=True, verbose_name=_("email")
    )
    first_name = models.CharField(max_length=255, verbose_name=_("first name"), default='')
    last_name = models.CharField(max_length=255, verbose_name=_("last name"), default='')
    business = models.ForeignKey(Business, on_delete=models.CASCADE, null=True, verbose_name=_("Business"))

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, verbose_name=_("role"))
    role_permissions = models.CharField(max_length=20, choices=ROLE_CHOICES, null=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]
    objects = UserManager()

    class Meta:
        # db_table = 'users'
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def set_permissions(self):
        Roles[self.role].permissions_func(self)
        self.role_permissions = self.role
        self.save()

    def __str__(self):
        return "{0} {1}".format(self.first_name, self.last_name)

    @staticmethod
    def check_role(sender, **kwargs):
        instance = kwargs.get("instance")
        created = kwargs.get("created")
        if not instance.id:
            return
        if instance.role_permissions != instance.role or created:
            instance.set_permissions()


post_init.connect(User.check_role, sender=User)
post_save.connect(User.check_role, sender=User)
# post_save.connect(User.add_recipient, sender=User)
# pre_delete.connect(User.delete_recipient, sender=User)
