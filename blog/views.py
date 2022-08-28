from datetime import timedelta, datetime

from django.db.models import Q, Count
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView

from account.mixins import PreviewMixin
from account.models import User
from blog.models import Article, Category, comment, Message


# Create your views here.


class Home(ListView):
    queryset = Article.objects.published()
    paginate_by = 5
    template_name = 'blog/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        last_month = datetime.today() - timedelta(days=30)
        context['month_popular_articles'] = Article.objects.published().annotate(
            count=Count('hits', filter=Q(articlehit__created__gt=last_month))) \
                                                .order_by('-count', '-publish')[:6]
        return context


class ArticleList(ListView):
    queryset = Article.objects.published()
    paginate_by = 5


class PopularList(ListView):
    paginate_by = 5
    template_name = 'blog/popular_list.html'

    def get_queryset(self):
        return Article.objects.published().annotate(count=Count('hits', filter=Q(hits__gt=0))) \
            .order_by('-count', '-publish')


class ArticleDetail(DetailView):
    def get_object(self):
        slug = self.kwargs.get('slug')
        article = get_object_or_404(Article.objects.published(), slug=slug)

        ip_address = self.request.user.ip_address
        if ip_address not in article.hits.all():
            article.hits.add(ip_address)

        return article

    def post(self, request, slug):
        article = get_object_or_404(Article.objects.published(), slug=slug)
        parent_id = request.POST.get('parent_id')
        body = request.POST.get('body')
        if parent_id == '':
            comment.objects.create(article=article, body=body, user=request.user)
        else:
            comment.objects.create(article=article, body=body, user=request.user, parent_id=int(parent_id))

        return redirect(self.request.path_info + '#comments')


class ArticlePreview(PreviewMixin, DetailView):
    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Article, pk=pk)


class CategoryList(ListView):
    paginate_by = 5
    template_name = 'blog/category_list.html'

    def get_queryset(self):
        global category
        slug = self.kwargs.get('slug')
        category = get_object_or_404(Category.objects.active(), slug=slug)
        return category.articles.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = category
        return context


class AuthorList(ListView):
    paginate_by = 5
    template_name = 'blog/author_list.html'

    def get_queryset(self):
        global author
        username = self.kwargs.get('username')
        author = get_object_or_404(User, username=username)
        return author.articles.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = author
        return context


class SearchList(ListView):
    paginate_by = 5
    template_name = 'blog/search_list.html'

    def get_queryset(self):
        search = self.request.GET.get('q')
        return Article.objects.published().filter(Q(description__icontains=search) |
                                                  Q(title__icontains=search) |
                                                  Q(author__first_name__icontains=search) |
                                                  Q(author__last_name__icontains=search))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('q')
        return context


class SidebarView(TemplateView):
    template_name = 'blog/includes/sidebar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['popular_articles'] = Article.objects.published().annotate(count=Count('hits')) \
                                          .order_by('-count', '-publish')[:4]
        context['categories'] = Category.objects.active()
        return context


class AboutUsView(TemplateView):
    template_name = 'blog/aboutus.html'


class ContactUsView(TemplateView):
    template_name = 'blog/contact.html'

    def post(self, request):
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        Message.objects.create(name=name, email=email, subject=subject, message=message)
        return redirect(self.request.path_info)
