from django import forms
from django.forms.widgets import ClearableFileInput as DjangoClearableFileInput

from .models import Comment, News


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


class ClearableFileInput(DjangoClearableFileInput):
    # template_name = "blocks/clearable_file_input.html"
    def _render(self, *args, **kwargs):
        r = super()._render(*args, **kwargs)
        r = r.replace("<br>", "</div><div>")
        return f"<div class='form-group-file'><div>{r}</div></div>"


class NewsForm(forms.ModelForm):
    image = forms.ImageField(
        required=False, widget=ClearableFileInput, label="Изображение"
    )

    class Meta:
        model = News
        fields = ("title", "description", "content", "image")
