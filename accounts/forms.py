from django import forms
from .models import CustomUser

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter Password',
            'class': 'form-control'
        })
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm Password',
            'class': 'form-control'
        })
    )

    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'phone_number',
            'email',
            'ward',
            'password',
        ]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
      

        # Password validation
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Password does not match!")
       
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add placeholders
        self.fields['first_name'].widget.attrs.update({
            'placeholder': 'Enter First Name',
            'class': 'form-control',
        })
        self.fields['last_name'].widget.attrs.update({
            'placeholder': 'Enter Last Name',
            'class': 'form-control',
        })
        self.fields['phone_number'].widget.attrs.update({
            'placeholder': 'Enter Phone Number',
            'class': 'form-control',
        })
        self.fields['email'].widget.attrs.update({
            'placeholder': 'Enter Email Address',
            'class': 'form-control',
        })
        self.fields['ward'].widget.attrs.update({
            'class': 'form-select',  
        })
