from django import forms
from django.core.validators import validate_slug
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
 
class RegistrationForm(forms.Form):
    username  = forms.CharField(label=_('Username'))
    email     = forms.EmailField(label=_('E-mail'))
    password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput(render_value=False))
    password2 = forms.CharField(label=('Confirm'), widget=forms.PasswordInput(render_value=False))

    def clean_username(self):
        username = self.cleaned_data['username']
        validate_slug(username)
        if User.objects.filter(username=username).count():
            raise forms.ValidationError(_("Username already exists"))
        return username

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise forms.ValidationError(_("Password not match"))
        return password2

class SignInForm(forms.Form):
    username = forms.CharField(label=_('Username'))
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput(render_value=False))
