from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from authorization.models import User
from business.models import Business


class CustomUserCreationForm(UserCreationForm):
    business = forms.ModelChoiceField(
        Business.objects.all(), required=False, label=_("Business")
    )

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "role", "business")

    def is_valid(self):
        check = super(CustomUserCreationForm, self).is_valid()
        if self.data["role"] != "global_admin" and not self.data["business"]:
            self.add_error("business", ValidationError(_("business should not be null")))
            check = False
        return check

    def clean_business(self):
        self.business = self.cleaned_data["business"]
        if self.business:
            self.business = self.business.id
        return self.business


class CustomUserChangeForm(UserChangeForm):
    business = forms.ModelChoiceField(
        Business.objects.all(), required=False, validators=[], label=_("Business")
    )

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "role", "business")

    def is_valid(self):
        check = super(CustomUserChangeForm, self).is_valid()
        if self.data["role"] != "global_admin" and not self.data["business"]:
            self.add_error("business", ValidationError(_("business should not be null")))
            check = False
        return check

    def clean_domain(self):
        self.business = self.cleaned_data["business"]
        if self.business:
            self.business = self.business.id
        return self.business


class SignUpForm(UserCreationForm):
    business = forms.CharField(max_length=200, required=True)
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2', )

    def is_valid(self):
        check = super(SignUpForm, self).is_valid()
        print(check)
        return check
