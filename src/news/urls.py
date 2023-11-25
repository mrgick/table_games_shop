from django.urls import path

from . import views

urlpatterns = [
    path("", views.NewsList.as_view(), name="news_list"),
    path("<int:pk>/", views.NewsDetail.as_view(), name="news_detail"),
    path("create/", views.NewsCreate.as_view(), name="news_create"),
    path("edit/<int:pk>/", views.NewsEdit.as_view(), name="news_edit"),
    path("delete/<int:pk>/", views.NewsDelete.as_view(), name="news_delete"),
    path("admin-news/", views.NewsAdminList.as_view(), name="admin_news")
]
