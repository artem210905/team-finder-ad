from django import forms
from django.contrib.auth import authenticate
from .models import User
import re

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label="Пароль")

    class Meta:
        model = User
        fields = ['name', 'surname', 'email', 'password']

    def save(self, commit=True):
        # Сохраняем пользователя, а паооль хешируем
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput(), label="Пароль")

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError("Неверный email или пароль")
            cleaned_data['user'] = user
        return cleaned_data

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'surname', 'avatar', 'about', 'phone', 'github_url']

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        # Проверяем формат (начинается на 8 или +7 и дальше 10 цифр)
        if not re.match(r'^(8|\+7)\d{10}$', phone):
            raise forms.ValidationError("Формат телефона: 8XXXXXXXXXX или +7XXXXXXXXXX")
        
        # Проверяем уникальность (те исключая самого себя)
        if User.objects.filter(phone=phone).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Этот номер уже используется другим пользователем")
        return phone

    def clean_github_url(self):
        url = self.cleaned_data.get('github_url')
        if url and 'github.com' not in url.lower():
            raise forms.ValidationError("Ссылка должна вести на GitHub")
        return url

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(), label="Старый пароль")
    new_password1 = forms.CharField(widget=forms.PasswordInput(), label="Новый пароль")
    new_password2 = forms.CharField(widget=forms.PasswordInput(), label="Повторите новый пароль")

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        cleaned_data = super().clean()
        old = cleaned_data.get('old_password')
        p1 = cleaned_data.get('new_password1')
        p2 = cleaned_data.get('new_password2')

        if old and not self.user.check_password(old):
            self.add_error('old_password', "Неверный старый пароль")
        if p1 and p2 and p1 != p2:
            self.add_error('new_password2', "Пароли не совпадают")
        return cleaned_data
