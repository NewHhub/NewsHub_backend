from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.utils.translation import gettext_lazy as _
from users.models import Followers

User = get_user_model()

class UserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")


class FollowForm(forms.ModelForm):
    class Meta:
        model = Followers
        fields = ("follow_by",)

class ProfileSettingsForm(forms.ModelForm):
    bio = forms.CharField(label='О себе', widget=forms.Textarea(attrs={'rows': 3}), max_length=500, required=False)
    avatar = forms.ImageField(label='Аватар', required=False)
    background = forms.ImageField(label='Фоновое изображение', required=False)
    first_name = forms.CharField(label='Имя', max_length=30, required=True)

    class Meta:
        model = User
        fields = ['bio', 'avatar', 'background', 'first_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bio'].initial = self.instance.bio
        self.fields['avatar'].initial = self.instance.avatar
        self.fields['background'].initial = self.instance.background
        self.fields['first_name'].initial = self.instance.first_name

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.bio = self.cleaned_data['bio']
        if self.cleaned_data['avatar']:
            user.avatar = self.cleaned_data['avatar']
        if self.cleaned_data['background']:
            user.background = self.cleaned_data['background']
        if commit:
            user.save()
        return user