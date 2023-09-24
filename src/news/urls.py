from django.urls import path

from . import views

urlpatterns = [
    path("", views.NewsList.as_view(), name="news_list"),
    path("<int:pk>/", views.NewsDetail.as_view(), name="news_detail"),
    path("edit/<int:pk>/", views.NewsEditDelete.as_view(), name="news_edit"),
    path("create/", views.CreateNews.as_view(), name="news_create"),
]
