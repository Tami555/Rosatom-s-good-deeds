from django import forms
from .models import Event
from django.utils import timezone


class EventCreateForm(forms.ModelForm):
    start_date = forms.DateTimeField(
        label='Дата и время начала',
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-input',
        }),
        input_formats=['%Y-%m-%dT%H:%M']
    )

    end_date = forms.DateTimeField(
        label='Дата и время окончания',
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-input',
        }),
        input_formats=['%Y-%m-%dT%H:%M']
    )

    class Meta:
        model = Event
        fields = ['title', 'description', 'start_date', 'end_date', 'image', 'address']
        labels = {
            'title': 'Название события',
            'description': 'Описание события',
            'image': 'Изображение события',
            'address': 'Адрес проведения',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Введите название события'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Подробное описание события',
                'rows': 5
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Адрес, где будет проходить событие'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-input'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            if start_date >= end_date:
                raise forms.ValidationError('Дата окончания должна быть позже даты начала')

            if start_date < timezone.now():
                raise forms.ValidationError('Нельзя создавать события в прошлом')

        return cleaned_data


class EventUpdateForm(forms.ModelForm):
    start_date = forms.DateTimeField(
        label='Дата и время начала',
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-input',
        }),
        input_formats=['%Y-%m-%dT%H:%M']
    )

    end_date = forms.DateTimeField(
        label='Дата и время окончания',
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-input',
        }),
        input_formats=['%Y-%m-%dT%H:%M']
    )

    class Meta:
        model = Event
        fields = ['title', 'description', 'start_date', 'end_date', 'image', 'address']
        labels = {
            'title': 'Название события',
            'description': 'Описание события',
            'image': 'Изображение события',
            'address': 'Адрес проведения',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Введите название события'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Подробное описание события',
                'rows': 5
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Адрес, где будет проходить событие'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-input'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            if start_date >= end_date:
                raise forms.ValidationError('Дата окончания должна быть позже даты начала')

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Для существующих событий разрешаем даты в прошлом
        if self.instance and self.instance.pk:
            # Можно убрать проверку на прошлые даты для редактирования
            pass