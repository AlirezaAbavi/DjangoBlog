from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html

from account.models import User


# my managers


class ArticleManager(models.Manager):
    def published(self):
        return self.filter(status='p')


class CommentManager(models.Manager):
    def published(self):
        return self.filter(status='p')


class CategoryManager(models.Manager):
    def active(self):
        return self.filter(status=True)


# Create your models here.
class IPAddress(models.Model):
    ip_address = models.GenericIPAddressField()


class Category(models.Model):
    parent = models.ForeignKey('self', default=None, null=True, blank=True, on_delete=models.SET_NULL,
                               related_name='children')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, unique=True)
    status = models.BooleanField(default=True)
    position = models.IntegerField()

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['parent__id', 'position']

    def __str__(self):
        return self.title

    objects = CategoryManager()


class Article(models.Model):
    STATUS_CHOICES = (
        ('d', 'Draft'),  # draft
        ('p', "Publish"),  # publish
        ('r', "Reviewing"),  # investigation
        ('b', "Denied"),  # back
    )
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='articles')
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, default='', blank=True)
    slug = models.SlugField(max_length=100, unique=True)
    category = models.ManyToManyField(Category, related_name="articles")
    description = models.TextField()
    thumbnail = models.ImageField(upload_to="images")
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_special = models.BooleanField(default=False, verbose_name='Special status')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    hits = models.ManyToManyField(IPAddress, through="ArticleHit", blank=True, related_name="hits")

    class Meta:
        ordering = ['-publish']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'slug': self.slug})

    def thumbnail_tag(self):
        return format_html("<img width=100 height=75 style='border-radius: 5px;' src='{}'>".format(self.thumbnail.url))

    thumbnail_tag.short_description = "thumbnail"

    def category_to_str(self):
        return ", ".join([category.title for category in self.category.active()])

    category_to_str.short_description = "Category"

    objects = ArticleManager()


class Comment(models.Model):
    STATUS_CHOICES = (
        ('p', "Publish"),  # publish
        ('r', "Reviewing"),  # investigation
        ('b', "Denied(Delete comment)"),  # back
    )

    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='r')

    class Meta:
        ordering = ['-article']

    def __str__(self):
        return self.body[:50]

    objects = CommentManager()


class ArticleHit(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    ip_address = models.ForeignKey(IPAddress, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True, editable=False)
    email = models.EmailField(null=True, blank=True, editable=False)
    subject = models.CharField(max_length=100, null=True, blank=True, editable=False)
    message = models.TextField(null=True, blank=True, editable=False)
