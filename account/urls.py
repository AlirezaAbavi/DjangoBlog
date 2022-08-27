from django.urls import path

from .views import ArticleList

app_name = 'account'

urlpatterns = [
    path('', ArticleList.as_view(), name='home'),
]
