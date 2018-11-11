from django import forms
from django.forms import widgets
from django.forms import fields
from .models import User


class RegisterForm(forms.Form):
    username = fields.CharField(widget=widgets.TextInput(),
                                label="用户")
    password = fields.CharField(widget=widgets.PasswordInput(),
                                label="密码")
    password_re = fields.CharField(widget=widgets.PasswordInput(),
                                   label="再次输入密码")
    answer = fields.CharField(widget=widgets.TextInput(),
                              label='密保问题您的生日（例如：20000101）',)


class LoginForm(forms.Form
                ):
    username = fields.CharField(widget=widgets.TextInput(),
                                label="用户")
    password = fields.CharField(widget=widgets.PasswordInput(),
                                label="密码")


class WriteForm(forms.Form):
    article_title_form = fields.CharField(label="文章标题")
    article_content_form = fields.CharField(widget=widgets.Textarea,
                                            label="文章内容")


class CommentForm(forms.Form):
    comment_content = fields.CharField(widget=widgets.Textarea,
                                       label="评论内容")


class ChangePasswordForm(forms.Form):
    old_password = fields.CharField(widget=widgets.PasswordInput(),
                                    label="旧密码")
    new_password = fields.CharField(widget=widgets.PasswordInput(),
                                    label="输入新密码")
    new_password_re = fields.CharField(widget=widgets.PasswordInput(),
                                       label="重新输入新密码")


class ForgetPasswordForm(forms.Form):
    username = fields.CharField(widget=widgets.TextInput(),
                                label="用户名")
    answer = fields.CharField(widget=widgets.TextInput(),
                              label="密保问题答案")
    new_password = fields.CharField(widget=widgets.PasswordInput(),
                                    label="输入新密码")
    new_password_re = fields.CharField(widget=widgets.PasswordInput(),
                                       label="重新输入新密码")
