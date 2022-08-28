from django.urls import path

from .views import (ArticleList,
                    ArticleCreate,
                    ArticleUpdate,
                    ArticleDelete,
                    Login,
                    )

app_name = 'account'

urlpatterns = [
    path('', ArticleList.as_view(), name='home'),
    path('login/', Login.as_view(), name='login'),
    path('article/new', ArticleCreate.as_view(), name='article-create'),
    path('article/edit/<int:pk>', ArticleUpdate.as_view(), name='article-update'),
    path('article/delete/<int:pk>', ArticleDelete.as_view(), name='article-delete'),
]
