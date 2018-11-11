
from django.contrib import admin
from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'password', 'answer',)


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('author', 'article_title', 'article_create_time', 'article_update_time')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment_man', 'comment_content', 'comment_article',)


class ToConfirmAdmin(admin.ModelAdmin):
    list_display = ('login_username', 'key',)


admin.site.register(User, UserAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(ToConfirm, ToConfirmAdmin)
