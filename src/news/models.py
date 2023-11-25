from io import BytesIO

from django.contrib.auth.models import User
from django.core.files import File
from django.core.files.base import ContentFile
from django.db import models
from django.urls import reverse
from django.utils import timezone
from PIL import Image


class News(models.Model):
    title = models.CharField(
        max_length=100, unique_for_date="date", verbose_name="Заголовок"
    )
    description = models.TextField(verbose_name="Краткое содержание")
    content = models.TextField(verbose_name="Полное содержание")
    date = models.DateTimeField(
        default=timezone.now, db_index=True, verbose_name="Опубликована"
    )
    author = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Автор"
    )
    image = models.ImageField(verbose_name="Изображение")

    def get_absolute_url(self):
        """Метод возвращает строку с URL-адресом записи."""
        return reverse("news_detail", args=[str(self.id)])

    def __str__(self):
        return self.title

    def compress_logo(self, image):
        im = Image.open(image)
        im_bytes = BytesIO()
        im.save(fp=im_bytes, format="WEBP", quality=100)
        image_content_file = ContentFile(content=im_bytes.getvalue())
        name = image.name.split(".")[0] + ".WEBP"
        new_image = File(image_content_file, name=name)
        return new_image

    def save(self, *args, **kwargs):
        try:
            object = News.objects.filter(id=self.id).first()
            if object and object.image != self.image:
                self.image = self.compress_logo(self.image)
                object.image.delete(save=False)
        except ValueError:
            pass
        super(News, self).save(*args, **kwargs)

    class Meta:
        db_table = "News"
        ordering = ["-date"]
        verbose_name = "новость"
        verbose_name_plural = "новости"
