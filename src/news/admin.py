from django.contrib import admin

from .models import Comment, News

admin.site.register(News)
admin.site.register(Comment)
