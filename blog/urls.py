from django.urls import path
from .views import (
    Home,
    ArticleList,
    PopularList,
    ArticleDetail,
    # ArticlePreview,
    CategoryList,
    AuthorList,
    SearchList,
    SidebarView,
    AboutUsView,
    ContactUsView,
)

app_name = "blog"
urlpatterns = [
    path('', Home.as_view(), name="home"),
    path('recent/', ArticleList.as_view(), name="list"),
    path('popular/', PopularList.as_view(), name="popular"),
    path('article/<slug:slug>', ArticleDetail.as_view(), name="detail"),
    # path('preview/<int:pk>', ArticlePreview.as_view(), name="preview"),
    path('category/<slug:slug>', CategoryList.as_view(), name="category"),
    path('author/<slug:username>', AuthorList.as_view(), name="author"),
    path('search/', SearchList.as_view(), name="search"),
    path('about', AboutUsView.as_view(), name="about"),
    path('contact', ContactUsView.as_view(), name="contact"),
    path('sidebar', SidebarView.as_view(), name="sidebar_partial"),
]
