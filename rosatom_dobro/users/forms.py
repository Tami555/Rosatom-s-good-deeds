from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from nko.models import City, Category, NKO


class VolunteerRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Введите ваш email'
        })
    )
    username = forms.CharField(
        label='Имя пользователя',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Придумайте имя пользователя'
        })
    )
    first_name = forms.CharField(
        required=True,
        label='Имя',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Ваше имя',
        })
    )
    last_name = forms.CharField(
        required=True,
        label='Фамилия',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Ваша фамилия'
        })
    )
    age = forms.IntegerField(
        required=True,
        label='Возраст',
        widget=forms.NumberInput(attrs={
            'class': 'form-input',
            'placeholder': 'Ваш возраст',
            'min': '14',
            'max': '100'
        })
    )
    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        required=True,
        label='Город',
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label="Выберите город"
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'age', 'city', 'password1', 'password2']
        labels = {
            'password1': 'Пароль',
            'password2': 'Подтверждение пароля',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Придумайте пароль'})
        self.fields['password2'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Повторите пароль'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'volunteer'
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class NKORegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label='Email организации',
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Email организации'
        })
    )
    username = forms.CharField(
        label='Имя пользователя',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Имя пользователя для входа'
        })
    )

    # Поля для модели NKO
    name = forms.CharField(
        max_length=200,
        label='Название НКО',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Название НКО'
        })
    )
    description = forms.CharField(
        label='Описание деятельности',
        widget=forms.Textarea(attrs={
            'class': 'form-input',
            'placeholder': 'Подробное описание деятельности',
            'rows': 4
        })
    )
    short_description = forms.CharField(
        max_length=300,
        label='Краткое описание',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Краткое описание (2-3 предложения)'
        })
    )
    logo = forms.ImageField(
        required=False,
        label='Логотип организации',
        widget=forms.FileInput(attrs={
            'class': 'form-input'
        })
    )
    address = forms.CharField(
        required=False,
        label='Адрес',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Адрес организации'
        })
    )
    website = forms.URLField(
        required=False,
        label='Веб-сайт',
        widget=forms.URLInput(attrs={
            'class': 'form-input',
            'placeholder': 'Сайт организации'
        })
    )
    vk_link = forms.URLField(
        required=False,
        label='ВКонтакте',
        widget=forms.URLInput(attrs={
            'class': 'form-input',
            'placeholder': 'Ссылка на ВКонтакте'
        })
    )
    telegram_link = forms.URLField(
        required=False,
        label='Telegram',
        widget=forms.URLInput(attrs={
            'class': 'form-input',
            'placeholder': 'Ссылка на Telegram'
        })
    )
    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        required=True,
        label='Город',
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label="Выберите город"
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=True,
        label='Категория деятельности',
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label="Выберите категорию"
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'password1': 'Пароль',
            'password2': 'Подтверждение пароля',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Придумайте пароль'})
        self.fields['password2'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Повторите пароль'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'nko'
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
            # Создаем запись НКО
            nko = NKO.objects.create(
                user=user,
                name=self.cleaned_data['name'],
                description=self.cleaned_data['description'],
                short_description=self.cleaned_data['short_description'],
                logo=self.cleaned_data['logo'],
                address=self.cleaned_data['address'],
                website=self.cleaned_data['website'],
                vk_link=self.cleaned_data['vk_link'],
                telegram_link=self.cleaned_data['telegram_link'],
                city=self.cleaned_data['city'],
                category=self.cleaned_data['category']
            )

        return user


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label='Имя пользователя',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Имя пользователя'
        })
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Пароль'
        })
    )


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'age', 'city']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Email',
            'age': 'Возраст',
            'city': 'Город',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ваше имя'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ваша фамилия'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Ваш email'}),
            'age': forms.NumberInput(
                attrs={'class': 'form-input', 'placeholder': 'Ваш возраст', 'min': '14', 'max': '100'}),
            'city': forms.Select(attrs={'class': 'form-select'}),
        }


class NKOUpdateForm(forms.ModelForm):
    class Meta:
        model = NKO
        fields = ['name', 'description', 'short_description', 'logo', 'address', 'website', 'vk_link', 'telegram_link',
                  'city', 'category']
        labels = {
            'name': 'Название НКО',
            'description': 'Описание деятельности',
            'short_description': 'Краткое описание',
            'logo': 'Логотип организации',
            'address': 'Адрес',
            'website': 'Веб-сайт',
            'vk_link': 'ВКонтакте',
            'telegram_link': 'Telegram',
            'city': 'Город',
            'category': 'Категория деятельности',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Название организации'}),
            'description': forms.Textarea(
                attrs={'class': 'form-input', 'rows': 4, 'placeholder': 'Подробное описание деятельности'}),
            'short_description': forms.TextInput(
                attrs={'class': 'form-input', 'placeholder': 'Краткое описание (2-3 предложения)'}),
            'logo': forms.FileInput(attrs={'class': 'form-input'}),
            'address': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Адрес организации'}),
            'website': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'https://example.com'}),
            'vk_link': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'https://vk.com/yourpage'}),
            'telegram_link': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'https://t.me/yourchannel'}),
            'city': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }