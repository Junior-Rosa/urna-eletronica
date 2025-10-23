from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from ..models import Eleitor


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="E-mail")

    identificador = forms.CharField(
        max_length=50,
        label="Identificador (CPF ou Título de Eleitor)",
        help_text="Informe um identificador único."
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'identificador']

    def save(self, commit=True):
        """Salva o usuário e cria automaticamente o Eleitor vinculado."""
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
            Eleitor.objects.create(
                user=user,
                identificador=self.cleaned_data['identificador']
            )
        return user
