from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}), label='')
    first_name = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}), label='')
    last_name = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}), label='')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['username'].label = ''
        self.fields['password1'].label = ''
        self.fields['password2'].label = ''
