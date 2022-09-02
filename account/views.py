from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from blog.models import Article, Comment
from .forms import ProfileForm, CommentForm
from .mixins import (
    FieldsMixin,
    FormValidMixin,
    AuthorAccessMixin,
    DeletionMixin,
    AuthorizedAccessMixin,
    CommentUpdateMixin
)
from .models import User


# Create your views here.


class ArticleList(AuthorizedAccessMixin, ListView):
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


class CommentList(AuthorizedAccessMixin, ListView):
    template_name = "registration/comment-list.html"
    context_object_name = 'Comments'

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return Comment.objects.all().order_by("-created_at", "article", "user")
        else:
            return Comment.objects.filter(article__author=self.request.user).order_by("-created_at", "article", "user")


class CommentUpdate(CommentUpdateMixin, UpdateView):
    model = Comment
    template_name = "registration/comment-update.html"
    form_class = CommentForm
    success_url = reverse_lazy("account:comment-list")

    def form_valid(self, form):
        comment = form.save(commit=False)
        if comment.status == 'b':
            comment.delete()
        else:
            # form.save(commit=True)
            return super().form_valid(form)
        return redirect('account:comment-list')

    def get_form_kwargs(self):
        kwargs = super(CommentUpdate, self).get_form_kwargs()
        kwargs.update({
            'user': self.request.user
        })
        return kwargs


class ArticleUpdate(AuthorAccessMixin, FieldsMixin, FormValidMixin, UpdateView):
    model = Article
    template_name = "registration/article-create-update.html"


class ArticleDelete(DeletionMixin, DeleteView):
    model = Article
    success_url = reverse_lazy('account:home')
    template_name = "registration/article_confirm_delete.html"


class Profile(LoginRequiredMixin, UpdateView):
    model = User
    template_name = "registration/profile.html"
    form_class = ProfileForm
    success_url = reverse_lazy("account:profile")

    def get_object(self):
        return User.objects.get(pk=self.request.user.pk)

    def get_form_kwargs(self):
        kwargs = super(Profile, self).get_form_kwargs()
        kwargs.update({
            'user': self.request.user
        })
        return kwargs


class Login(LoginView):
    def get_success_url(self):
        user = self.request.user

        if not self.request.POST.get('remember-me'):
            self.request.session.set_expiry(0)

        if user.is_superuser or user.is_staff or user.is_author:
            return reverse_lazy("account:home")
        else:
            return reverse_lazy("account:profile")


from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage


class Register(CreateView):
    form_class = SignupForm
    template_name = "registration/register.html"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        mail_subject = 'Activate your Django Blog account.'
        message = render_to_string('registration/account_activation_email.html', context={
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        return render(self.request, 'registration/account_activation_done.html')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        is_done = True
    else:
        is_done = False
    return render(request, 'registration/account_activation_complete.html', context={'is_done': is_done})
