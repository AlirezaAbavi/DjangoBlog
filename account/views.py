from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView

from blog.models import Article
from .mixins import FieldsMixin, FormValidMixin, AuthorAccessMixin


# Create your views here.
class ArticleList(LoginRequiredMixin, ListView):
    template_name = "registration/article_list.html"
    context_object_name = 'Articles'

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return Article.objects.all()
        else:
            return Article.objects.filter(author=self.request.user)


class ArticleCreate(LoginRequiredMixin, FieldsMixin, FormValidMixin, CreateView):
    model = Article
    template_name = "registration/article-create-update.html"


class ArticleUpdate(AuthorAccessMixin, FieldsMixin, FormValidMixin, UpdateView):
    model = Article
    template_name = "registration/article-create-update.html"
