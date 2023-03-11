from django import forms
from blog.models import Post, Like

class LikeForm(forms.ModelForm):
    class Meta:
        model = Like
        fields = ("post",)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "text", "poster")