from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser


class RegisterForm(UserCreationForm):
    ROLE_CHOICES = [
        ('customer', 'Customer - Find local services'),
        ('provider', 'Provider - Offer your services'),
    ]

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'role-radio'}),
        initial='customer'
    )
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=False)
    city = forms.CharField(max_length=100, required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone', 'city', 'role', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if hasattr(field.widget, 'attrs') and field.widget.__class__.__name__ != 'RadioSelect':
                field.widget.attrs.update({'class': 'form-input'})


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Username'})
        self.fields['password'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Password'})


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone', 'bio', 'avatar', 'city', 'state', 'location']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'phone': forms.TextInput(attrs={'class': 'form-input'}),
            'city': forms.TextInput(attrs={'class': 'form-input'}),
            'state': forms.TextInput(attrs={'class': 'form-input'}),
            'location': forms.TextInput(attrs={'class': 'form-input'}),
        }
