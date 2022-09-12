from django.contrib import admin
from business.models import Business
from django.contrib.admin import SimpleListFilter
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin
from authorization.models import User
# from tes/t_app.a
# Register your models here.
from .forms import CustomUserChangeForm, CustomUserCreationForm, SignUpForm

class BusinessListFilter(SimpleListFilter):
    title = _("Business")
    parameter_name = "business"

    default_value = None

    def lookups(self, request, model_admin):
        list_of_business = []
        queryset = Business.objects.all()
        for business in queryset:
            list_of_business.append((str(business.id), str(business)))
        return sorted(list_of_business, key=lambda tp: tp[1])

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(business=self.value())
        return queryset


class MyUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = SignUpForm
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {
                "fields": ("role", "business"),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {
                "fields": ("role", "business"),
            },
        ),
    )
    list_display = [
        "email",
        "first_name",
        "last_name",
        "role",
        "business",
    ]
    list_filter = ("role", BusinessListFilter)
    search_fields = ("first_name", "last_name", "email", 'business')
    ordering = ("last_name",)
    filter_horizontal = ()


admin.site.register(User, MyUserAdmin)