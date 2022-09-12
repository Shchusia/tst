from django.contrib.auth.models import Permission

def get_global_admin_permissions(obj):
    obj.is_superuser = True


def get_global_manager_permissions(obj):
    obj.is_superuser = True


def get_business_admin_permissions(obj):
    obj.is_superuser = False
    permissions = list()
    permissions.extend(
      Permission.objects.filter(content_type__model="business").all()
    )
    permissions.extend(
      Permission.objects.filter(content_type__model="businesses_product").all()
    )
    permissions.extend(
        Permission.objects.filter(content_type__model="businesses_news").all()
    )
    obj.user_permissions.set(permissions)


def get_business_manager_permissions(obj):
    obj.is_superuser = False
    permissions = list()
    permissions.extend(
        Permission.objects.filter(content_type__model="businesses_product").all()
    )
    obj.user_permissions.set(permissions)
