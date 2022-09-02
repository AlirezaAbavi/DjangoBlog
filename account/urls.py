from django.urls import path

from .views import (ArticleList,
                    ArticleCreate,
                    ArticleUpdate,
                    ArticleDelete,
                    Profile,
                    CommentList,
                    CommentUpdate,
                    )

app_name = 'account'

urlpatterns = [
    path('', ArticleList.as_view(), name='home'),
    path('comments/', CommentList.as_view(), name='comment-list'),
    path('comments/<int:pk>', CommentUpdate.as_view(), name='comment-update'),
    path('article/new', ArticleCreate.as_view(), name='article-create'),
    path('article/edit/<int:pk>', ArticleUpdate.as_view(), name='article-update'),
    path('article/delete/<int:pk>', ArticleDelete.as_view(), name='article-delete'),
    path('profile/', Profile.as_view(), name="profile"),
]
