from django.db import models
from django.utils import timezone


class User(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    answer = models.CharField(max_length=8)


class Article(models.Model):
    author = models.ForeignKey(User)
    article_title = models.CharField(max_length=100)
    article_content = models.CharField(max_length=10000)
    article_create_time = models.DateTimeField(default=timezone.now)
    article_update_time = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    comment_content = models.CharField(max_length=300)
    comment_man = models.ForeignKey(User)
    comment_article = models.ForeignKey(Article)
    comment_create_time = models.DateTimeField(default=timezone.now)


class Main(models.Model):
    all_article = models.ForeignKey(Article)
    all_comment = models.ForeignKey(Comment)


class ToConfirm(models.Model):
    login_username = models.CharField(max_length=10000)
    key = models.CharField(max_length=10)
    create_time = models.DateTimeField(default=timezone.now)

