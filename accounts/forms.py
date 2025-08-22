from django import forms
from .models import CustomUser
from complaints.models import Ward

class RegistrationForm(forms.ModelForm):
    # Ward dropdown
    ward = forms.ModelChoiceField(
        queryset=Ward.objects.select_related('municipality').all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label="Select Ward",
        required=True
    )

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
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'ward', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match!")

        # Ensure a ward is selected
        ward = cleaned_data.get('ward')
        if not ward:
            raise forms.ValidationError("Please select a ward.")

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add placeholders and Bootstrap classes
        for field_name in ['first_name', 'last_name', 'phone_number', 'email']:
            self.fields[field_name].widget.attrs.update({
                'placeholder': f'Enter {field_name.replace("_", " ").title()}',
                'class': 'form-control'
            })
        self.fields['password'].widget.attrs.update({'class': 'form-control'})
        self.fields['confirm_password'].widget.attrs.update({'class': 'form-control'})
