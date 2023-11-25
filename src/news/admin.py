from django.contrib import admin

from .models import News


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display= ("title", "author", "date")
    list_filter = ("author",)
    search_fields = ("title",)

