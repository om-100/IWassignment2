from django import forms
from django.contrib.auth import get_user_model
from .models import Blog

User = get_user_model()


class Register_form(forms.ModelForm):
    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 8:
            raise forms.ValidationError("must be 8 character")
        return password

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'image']

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'username': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'email': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'email'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control'

            })

        }


class Loginform(forms.Form):
    email = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'email'
    }))
    password = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'image', 'content']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control'
            }),

        }
