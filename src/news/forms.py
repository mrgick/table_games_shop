from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    text = forms.CharField(
        label="Комментарий",
        required=True,
        widget=forms.Textarea,
    )

    class Meta:
        model = Comment
        fields = ("text",)
        labels = {"text": "Комментарий"}


# class NewsForm(forms.ModelForm):
#     image = forms.FileField(required=False, label="Изображение")

#     class Meta:
#         model = News
#         fields = ("title", "description", "content", "image")
#         labels = {
#             "title": "Заголовок",
#             "description": "Краткое содержание",
#             "content": "Полное содержание",
#             "image": "Изображение",
#         }
