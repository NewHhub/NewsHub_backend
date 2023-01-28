from django import forms
from blog.models import Post, Like

class LikeForm(forms.ModelForm):
    class Meta:
        model = Like
        fields = ("post",)
