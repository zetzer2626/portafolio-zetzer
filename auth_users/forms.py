from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Personalizar widgets con clases Bootstrap
        self.fields['username'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu nombre de usuario',
            'autocomplete': 'username'
        })
        
        self.fields['password1'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu contraseña',
            'autocomplete': 'new-password'
        })
        
        self.fields['password2'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirma tu contraseña',
            'autocomplete': 'new-password'
        })
        
        # Personalizar labels
        self.fields['username'].label = 'Nombre de Usuario'
        self.fields['password1'].label = 'Contraseña'
        self.fields['password2'].label = 'Confirmar Contraseña'
        
        # Personalizar help_text
        self.fields['username'].help_text = 'Requerido. 150 caracteres o menos. Solo letras, dígitos y @/./+/-/_'
        self.fields['password1'].help_text = '''
        <ul class="form-text">
            <li>Tu contraseña no puede ser muy similar a tu información personal.</li>
            <li>Tu contraseña debe contener al menos 8 caracteres.</li>
            <li>Tu contraseña no puede ser una contraseña común.</li>
            <li>Tu contraseña no puede ser completamente numérica.</li>
        </ul>
        '''
        self.fields['password2'].help_text = 'Ingresa la misma contraseña que antes, para verificación.' 