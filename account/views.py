from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from blog.models import Article


# Create your views here.
class ArticleList(LoginRequiredMixin, ListView):
    template_name = "registration/home.html"
    context_object_name = 'Articles'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Article.objects.all()
        else:
            return Article.objects.filter(author=self.request.user)


