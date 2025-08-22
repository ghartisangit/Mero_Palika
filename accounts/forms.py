from django import forms
from .models import CustomUser

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password',
        'class': 'form-control',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password',
        'class': 'form-control',
    }))

    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'phone_number',
            'email',
            'municipality',
            'ward',
            'password',
        ]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        municipality = cleaned_data.get('municipality')
        ward = cleaned_data.get('ward')

     
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Password does not match!")

    
        if not municipality:
            raise forms.ValidationError("Municipality is required.")
        if not ward:
            raise forms.ValidationError("Ward is required.")

        return cleaned_data  

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'

    
        self.fields['municipality'].widget.attrs['class'] = 'form-select'
        self.fields['ward'].widget.attrs['class'] = 'form-select'

       
        for field in self.fields:
            if field not in ['municipality', 'ward']:
                self.fields[field].widget.attrs['class'] = 'form-control'
