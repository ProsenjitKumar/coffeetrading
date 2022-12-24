from django.contrib.auth.models import User
from django import forms
from django.forms import TextInput, PasswordInput
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, DepositConfirmation


class SignupForm(UserCreationForm):

    password1 = forms.CharField(label='Password', widget=forms.TextInput(attrs={"type": "password", 'placeholder': ("Password")}))
    password2 = forms.CharField(label='Password confirmation', widget=forms.TextInput(attrs={"type": "password", 'placeholder': ("Confirm Password")}))

    class Meta:
        model = User
        fields = ('username', 'email')

        widgets = {
            'username': TextInput(attrs={'placeholder': 'Username'}),

        }


class LoginForm(forms.Form):
    username = forms.CharField(label='Email', widget=forms.TextInput(attrs={'placeholder': ("Username")}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': ("Your Password")}), label='Password')

    def clean_login(self):
        if self.username and self.password:
            raise forms.ValidationError("Password or Email Incorrect.")


# -------------------------------
#                                |
#     Profile Update
#                                |
# -------------------------------
class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    email = forms.EmailField()

    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user']


def form_validation_error(form):
    msg = ""
    for field in form:
        for error in field.errors:
            msg += "%s: %s \\n" % (field.label if hasattr(field, 'label') else 'Error', error)
    return msg

# -------------------------------
#                                |
#     Deposit Confirmation Form
#                                |
# -------------------------------


class DepositConfirmationForm(forms.ModelForm):
    class Meta:
        model = DepositConfirmation
        fields = '__all__'
        exclude = ['investor_user_name']