from django import forms
from django.contrib.auth.forms import UserCreationForm

from ads.models import Ad, Category


class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ('title', 'description', 'price', 'category')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 6}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].required = True
        self.fields['category'].empty_label = 'Выберите категорию'


class AdFilterForm(forms.Form):
    q = forms.CharField(
        required=False,
        label='Поиск',
        widget=forms.TextInput(attrs={
            'type': 'search',
            'class': 'form-control',
            'placeholder': 'Поиск по заголовку и описанию',
        }),
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label='Все категории',
        label='Категория',
        widget=forms.Select(attrs={
            'class': 'form-select',
            'style': 'max-width: 220px',
            'onchange': 'this.form.submit()',
        }),
    )


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ('username',)
