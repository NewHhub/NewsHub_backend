from django import forms
from blog.models import Post, Like, Reviews, Reviews_like

class LikeForm(forms.ModelForm):
    class Meta:
        model = Like
        fields = ("post",)

class LikeReviewForm(forms.ModelForm):
    class Meta:
        model = Reviews_like
        fields = ("review",)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "text", "poster")


class CommentForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ("post", "text", "parent", "tread")