from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

CustomUser = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    """Form for custom user creation."""
    class Meta:
        model = CustomUser
        fields = ('email', 'username')


class CustomUserChangeForm(UserChangeForm):
    """Form for custom user information edit."""
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'about_me')
