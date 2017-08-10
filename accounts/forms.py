from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
)
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

from accounts.models import User


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords don\'t match')
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'name',
            'avatar',
            'gender',
            'date_of_birth',
            'contact',
            'quote',
        )
    def save(self, commit=True):
        user = super(UserChangeForm, self).save(commit=False)
        if commit:
            user.save()
        return user

class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username',
            'email',
            'password1',
            'password2',
            'avatar',
            'gender',
            'date_of_birth',
            'contact',
            'quote',
            Submit('signup', 'Sign up', css_class='btn primary')
        )


class UpdateAccountForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(UpdateAccountForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username',
            'email',
            'name',
            'avatar',
            'gender',
            'date_of_birth',
            'contact',
            'quote',
            Submit('update', 'Update Account', css_class='btn primary')
        )


class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        user = kwargs['initial']['user']
        super(ChangePasswordForm, self).__init__(user, *args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'old_password',
            'new_password1',
            'new_password2',
            Submit('update', 'Update Password', css_class='btn primary')
        )


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username',
            'password',
            Submit('login', 'Login', css_class='btn-primary')
        )
