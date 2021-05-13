from django import forms
from .models import CustomUser


from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm

from django.utils.translation import gettext, gettext_lazy as _

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)

#class SignupForm(forms.Form):
#    full_name = forms.CharField(label='Full Name', max_length=30)
#    email = forms.EmailField(label='Email')
#    ph_no = forms.CharField(label='Ph. No.', max_length=15)
#    password = forms.CharField(label='Password', max_length=100)
#    confirm_password = forms.CharField(label='Confirm Password', max_length=100)


class SignupForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name','last_name', 'username', 'email', 'ph_no', 'password']

    confirm_password = forms.CharField(label='Confirm Password', max_length=100)


class UserRegisterForm(UserCreationForm):
    #email = forms.EmailField()
    #ph_no = forms.CharField(max_length = 20)
    #full_name = forms.CharField(max_length = 20)
    class Meta:
        model = CustomUser
        fields = ['first_name','last_name', 'username',  'email', 'ph_no']



class UserRegisterLiteForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email']
        #fields = []


class LoginForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'password']



class LoginForm(AuthenticationForm):
    #email = forms.CharField(label='Email ID')
    class Meta:
        model = CustomUser
        fields = [ 'email']

class PasswordChangeForm(AuthenticationForm): #(UserCreationForm):
    old_password = forms.CharField(
        label=_("Old Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )
    class Meta:
        model = CustomUser
        fields = ['email', 'old_password', 'password1', 'password2']

    field_order = ['email', 'old_password', 'password1', 'password2']


class PasswordResetForm(SetPasswordForm):

    new_password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )
    new_password2 = forms.CharField(
        label=_("Re-Enter Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )

    field_order = ['new_password1', 'new_password2']


class PasswordResetOtpForm(SetPasswordForm):
    otp = forms.CharField(
        label=_("Email OTP"),
        max_length=30,
    )
    new_password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )
    new_password2 = forms.CharField(
        label=_("Re-Enter Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )

    field_order = ['otp', 'new_password1', 'new_password2']


class PasswordForgetForm(forms.Form):
    email = forms.EmailField(
        label=_("Email "),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    )
    
    
    
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'ph_no']
