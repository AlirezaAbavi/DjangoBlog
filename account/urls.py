from django.urls import path

from .views import ArticleList, ArticleCreate, ArticleUpdate

app_name = 'account'

urlpatterns = [
    path('', ArticleList.as_view(), name='home'),
    path('article/new', ArticleCreate.as_view(), name='article-create'),
    path('article/edit/<int:pk>', ArticleUpdate.as_view(), name='article-update'),

]
