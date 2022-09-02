from django.http import Http404
from django.shortcuts import get_object_or_404, redirect

from blog.models import Article, Comment


class FieldsMixin():
    def dispatch(self, request, *args, **kwargs):
        self.fields = [
            "title", "subtitle", "slug", "category",
            "description", "thumbnail", "publish",
            "is_special", "status"
        ]
        if request.user.is_superuser or request.user.is_staff:
            self.fields.append("author")
        return super().dispatch(request, *args, **kwargs)


class FormValidMixin():
    def form_valid(self, form):
        if self.request.user.is_superuser or self.request.user.is_staff:
            form.save()
        else:
            self.obj = form.save(commit=False)
            self.obj.author = self.request.user
            if not self.obj.status == 'r':
                self.obj.status = 'd'
        return super().form_valid(form)


class AuthorAccessMixin():
    def dispatch(self, request, pk, *args, **kwargs):
        article = get_object_or_404(Article, pk=pk)
        if article.author == request.user \
                or request.user.is_superuser \
                or request.user.is_staff \
                or article.status in ['d', 'b', 'p']:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("YOU ARE NOT AUTHORIZED FOR THIS ACTION")


class DeletionMixin():
    def dispatch(self, request, pk, *args, **kwargs):
        article = get_object_or_404(Article, pk=pk)
        if request.user.is_superuser or request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)
        elif request.user == article.author and article.status in ['d', 'r', 'b']:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("YOU ARE NOT AUTHORIZED FOR THIS ACTION")


class PreviewMixin():
    def dispatch(self, request, pk, *args, **kwargs):
        article = get_object_or_404(Article, pk=pk)
        if article.status == 'p':
            return redirect('blog:detail', article.slug)
        elif request.user.is_superuser \
                or request.user.is_staff \
                or request.user == article.author \
                and article.status in ['d', 'r', 'b']:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("YOU ARE NOT AUTHORIZED FOR THIS ACTION")


class AuthorizedAccessMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_author \
                or request.user.is_superuser \
                or request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('account:profile')


class CommentUpdateMixin():
    def dispatch(self, request, pk, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=pk)
        if comment.article.author == request.user \
                or request.user.is_superuser \
                or request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)
        elif request.user.is_author:
            return redirect('account:comment-list')
        else:
            raise Http404("YOU ARE NOT AUTHORIZED FOR THIS SECTION")
