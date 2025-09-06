from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import News_post, PendingNews


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Добавляем Bootstrap классы
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            
        # Настраиваем placeholder'ы
        self.fields['username'].widget.attrs['placeholder'] = 'Имя пользователя'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Имя'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Фамилия'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['password1'].widget.attrs['placeholder'] = 'Пароль'
        self.fields['password2'].widget.attrs['placeholder'] = 'Подтверждение пароля'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Добавляем Bootstrap классы
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            
        # Настраиваем placeholder'ы
        self.fields['username'].widget.attrs['placeholder'] = 'Имя пользователя'
        self.fields['password'].widget.attrs['placeholder'] = 'Пароль'


class NewsApprovalForm(forms.ModelForm):
    """Форма для одобрения новостей из интернета"""
    approve = forms.BooleanField(
        label='Одобрить новость',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    class Meta:
        model = News_post
        fields = ['title', 'short_description', 'text', 'author']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'short_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'author': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ограничиваем выбор авторов только активными пользователями
        self.fields['author'].queryset = User.objects.filter(is_active=True)


class LoadNewsForm(forms.Form):
    """Форма для загрузки новостей из интернета"""
    count = forms.IntegerField(
        label='Количество новостей',
        min_value=1,
        max_value=10,
        initial=5,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['count'].help_text = 'Укажите количество новостей для загрузки (от 1 до 10)'
