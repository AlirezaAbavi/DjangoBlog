import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm

from account.models import User


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')

        super(ProfileForm, self).__init__(*args, **kwargs)

        remaining_days = (user.special_user - datetime.datetime.now(datetime.timezone.utc)).days
        if remaining_days > 0:
            self.fields['special_user'].help_text = f'Your subscription expires in {remaining_days} days.'
        else:
            self.fields['special_user'].help_text = f'Your subscription has expired.'
        self.fields['is_author'].help_text = "Designates whether this user should be treated as author."
        self.fields['is_staff'].help_text = "Designates whether this user is authorized to access privileged sections"

        if not user.is_superuser:
            self.fields['username'].help_text = None
            self.fields['username'].disabled = True
            self.fields['special_user'].disabled = True
            self.fields['is_author'].disabled = True
            self.fields['is_active'].disabled = True
            self.fields['is_superuser'].disabled = True
            self.fields['is_staff'].disabled = True
            self.fields['last_login'].disabled = True

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name',
                  'special_user', 'is_author', 'is_superuser', 'is_staff', 'is_active', 'last_login']


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
