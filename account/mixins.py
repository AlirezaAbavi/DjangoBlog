from django.http import Http404
from django.shortcuts import get_object_or_404

from blog.models import Article


class FieldsMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.is_staff:
            self.fields = [
                "title", "subtitle", "slug", "category",
                "description", "thumbnail", "publish",
                "is_special", "status", "author"
            ]
        elif request.user.is_author:
            self.fields = [
                "title", "slug", "category",
                "description", "thumbnail", "publish",
                "is_special"
            ]
        else:
            raise Http404("YOU ARE NOT AUTHORIZED FOR THIS SECTION")
        return super().dispatch(request, *args, **kwargs)


class FormValidMixin():
    def form_valid(self, form):
        if self.request.user.is_superuser or self.request.user.is_staff:
            form.save()
        else:
            self.obj = form.save(commit=False)
            self.obj.author = self.request.user
            self.obj.status = 'r'
        return super().form_valid(form)


class AuthorAccessMixin():
    def dispatch(self, request, pk, *args, **kwargs):
        article = get_object_or_404(Article, pk=pk)
        if article.author == request.user \
                or request.user.is_superuser \
                or request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("YOU ARE NOT AUTHORIZED FOR THIS ACTION")
