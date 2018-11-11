from django.shortcuts import render
from .forms import *
from .models import *
import random
import string
import datetime
import re


def clean_cookie():
    the_all = ToConfirm.objects.all()
    for one in the_all:
        if one.create_time.replace(tzinfo=None) + datetime.timedelta(hours=8, minutes=10) < \
                datetime.datetime.now().replace(tzinfo=None):
            one.delete()


def confirm_cookie(request, rs):
    clean_cookie()
    if request.COOKIES.get("key"):
        cookie_key = request.COOKIES.get("key")
        result = ToConfirm.objects.filter(key=cookie_key)
        if len(result) != 0:
            rs = result[0].login_username
            return rs
    else:
        pass


def test_register(username, password, password_re, answer):
        result = ""
        if username == "" or password == "" or password_re == "" or answer == "":
            result = "请输入用户名、密码、密保问题答案"
            return {"result": result, "username": username, "answer": answer}
        else:
            if len(username) >= 6 and len(password) >= 6:
                if re.search(r'\W', username) or re.search(r'[A-Z]', username):
                    result = "用户名必须由小写字母、数字或下划线组成"
                    return {"result": result, "username": username, "answer": answer}
                else:
                    if re.search(r' ', password):
                        result = "密码不能含有空格"
                        return {"result": result, "username": username, "answer": answer}
                    else:
                        if re.search(r'[a-zA-Z]', password) and re.search(r'[0-9]', password):
                            if len(User.objects.filter(username=username)) != 0:
                                result = "用户名已经被注册"
                                return {"result": result, "username": username, "answer": answer}
                            if password == password_re:
                                result = "YES"
                                return {"result": result}
                            else:
                                result = "两次输入的密码不同"
                                return {"result": result, "username": username, "answer": answer}
                        else:
                            result = "密码必须含有字母和数字"
                            return {"result": result, "username": username, "answer": answer}
            else:
                result = "用户名或密码过短"
                return {"result": result, "username": username, "answer": answer}


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            password_re = form.cleaned_data["password_re"]
            answer = form.cleaned_data["answer"]
            register_user = User(username=form.cleaned_data["username"],
                                 password=form.cleaned_data["password"],
                                 answer=form.cleaned_data["answer"])
            result = test_register(username, password, password_re, answer)
            if result["result"] == "YES":
                register_user.save()
                result = "注册成功"
                return render(request, "RegisterPage.html", {"result": result, "form": form})
            else:
                result.update({"form": form})
                return render(request, "RegisterPage.html", result)
    else:
        form = RegisterForm()
    return render(request, "RegisterPage.html", {"form": form})


def login(request):
    rs = ""
    rs = confirm_cookie(request, rs)
    if rs is not None:
        result = "您已登陆"
        return render(request, "Welcome.html", {"username": rs, "result": result})
    if request.method == 'POST':
        form = LoginForm(request.POST)
        form.is_valid()
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        man = User.objects.filter(username=username)
        if len(man) != 0:
            if man[0].password == password:
                random_number = ''.join(random.sample(string.ascii_letters + string.digits, 10))
                response = render(request, "Welcome.html", {"form": form})
                response.set_cookie("key", random_number, 3600, '/')
                cookie_save = ToConfirm(login_username=username, key=random_number)
                cookie_save.save()
                return response
            else:
                result = "密码错误"
                return render(request, "LoginPage.html", {"form": form, "result": result})
        else:
            result = "用户不存在"
            return render(request, "LoginPage.html", {"form": form, "result": result})
    else:
        form = LoginForm()
    return render(request, "LoginPage.html", {"form": form})


def write(request):
    result = ""
    rs = ""
    rs = confirm_cookie(request, rs)
    if rs is None:
        result = "请先登陆"
        return render(request, "Welcome.html", {"result": result})
    if request.method == 'POST':
        form = WriteForm(request.POST)
        form.is_valid()
        article_to_save = Article(author=User.objects.get(username=rs),
                                  article_title=form.cleaned_data["article_title_form"],
                                  article_content=form.cleaned_data["article_content_form"])
        article_to_save.save()
        result = "成功提交"
    else:
        form = WriteForm()
    return render(request, "WritePage.html", {"form": form, "result": result})


def article_list(request):
    article = Article.objects.all()
    the_article = {'article': article}
    return render(request, 'ArticleList.html', the_article)


def article_page(request, id):
    result = ""
    article = Article.objects.get(id=id)
    if len(Comment.objects.filter(comment_article=article)) != 0:
        comment = Comment.objects.filter(comment_article=article)
    else:
        comment = {}
        result = "无评论"
    everything_article = {"article": article, "comment": comment, "result": result}
    return render(request, "Article.html", everything_article)


def to_delete_cookie(request):
    if request.COOKIES.get("key"):
        cookie = ToConfirm.objects.filter(key=request.COOKIES.get("key"))
        cookie.delete()
    response = render(request, "Welcome.html")
    response.delete_cookie("key")
    return response


def to_comment(request, id):
    rs = ""
    rs = confirm_cookie(request, rs)
    if rs is None:
        result = "请先登陆"
        return render(request, "Welcome.html", {"result": result})
    if request.method == "POST":
        form = CommentForm(request.POST)
        form.is_valid()
        article = Article.objects.get(id=id)
        comment_to_save = Comment(comment_man=User.objects.get(username=rs),
                                  comment_content=form.cleaned_data["comment_content"],
                                  comment_article=Article.objects.get(id=id))
        comment_to_save.save()
        result = "评论成功"
        return render(request, "Article.html", {"form": form, "id": id, "result": result, "article": article})
    else:
        form = CommentForm()
    return render(request, "Comment.html", {"form": form, "id": id})


def welcome_page(request):
    return render(request, "Welcome.html")


def edit_article(request, id):
    rs = ""
    rs = confirm_cookie(request, rs)
    if rs is None:
        result = "请先登陆"
        return render(request, "Welcome.html", {"result": result, "id": id})
    if rs != Article.objects.get(id=id).author.username:
        article = Article.objects.get(id=id)
        result = "您没有权限修改文章"
        return render(request, "Article.html", {"result": result, "id": id, "article": article})
    if request.method == "POST":
        form = WriteForm(request.POST)
        form.is_valid()
        article = Article.objects.get(id=id)
        article.article_content = request.POST.get("new_content")
        article.article_title = request.POST.get("new_title")
        article.save()
        result = "修改成功"
        return render(request, "Article.html", {"result": result, "id": id, "form": form, "article": article})
    else:
        article = Article.objects.get(id=id)
        form = WriteForm()
        form.article_content = article.article_content
        form.article_title = article.article_title
        return render(request, "EditArticle.html", {"form": form, "id": id})


def delete_article(request, id):
    rs = ""
    rs = confirm_cookie(request, rs)
    if rs is None:
        result = "请先登陆"
        return render(request, "Welcome.html", {"result": result})
    if rs != Article.objects.get(id=id).author.username:
        article = Article.objects.get(id=id)
        result = "您没有权限删除文章"
        return render(request, "Article.html", {"result": result, "id": id, "article": article})
    article = Article.objects.get(id=id)
    comment = Comment.objects.filter(comment_article=article)
    comment.delete()
    article.delete()
    return render(request, "ArticleList.html")


def password_test(password):
    if len(password) >= 6:
        if re.search(r' ', password):
            result = "密码不能含有空格"
            return result
        else:
            if re.search(r'[a-zA-Z]', password) and re.search(r'[0-9]', password):
                result = "YES"
                return result
            else:
                result = "密码必须含有字母和数字"
                return result
    else:
        result = "密码过短"
        return result


def change_password(request):
    rs = ""
    rs = confirm_cookie(request, rs)
    if rs is None:
        result = "请先登陆"
        return render(request, "Welcome.html", {"result": result})
    if request.method == "POST":
        form = ChangePasswordForm(request.POST)
        form.is_valid()
        old_password = form.cleaned_data["old_password"]
        new_password = form.cleaned_data["new_password"]
        new_password_re = form.cleaned_data["new_password_re"]
        if old_password == User.objects.get(username=rs).password:
            if new_password == new_password_re:
                result = password_test(new_password)
                if result == "YES":
                    user = User.objects.get(username=rs)
                    user.password = new_password
                    user.save()
                    result = "修改成功"
                    return render(request, "ChangePassword.html", {"form": form, "result": result})
                else:
                    return render(request, "ChangePassword.html", {"form": form, "result": result})
            else:
                result = "两次输入的密码不同"
                return render(request, "ChangePassword.html", {"form": form, "result": result})
        else:
            result = "密码错误"
            return render(request, "ChangePassword.html", {"form": form, "result": result})
    else:
        form = ChangePasswordForm()
    return render(request, "ChangePassword.html", {"form": form})


def forget_password(request):
    if request.method == "POST":
        form = ForgetPasswordForm(request.POST)
        form.is_valid()
        username = form.cleaned_data["username"]
        answer = form.cleaned_data["answer"]
        new_password = form.cleaned_data["new_password"]
        new_password_re = form.cleaned_data["new_password_re"]
        user = User.objects.filter(username=username)
        if len(user) != 0:
            if answer == user[0].answer:
                if new_password == new_password_re:
                    result = password_test(new_password)
                    if result == "YES":
                        user = User.objects.get(username=username)
                        user.password = new_password
                        user.save()
                        result = "修改成功"
                        return render(request, "ForgetPassword.html", {"form": form, "result": result})
                    else:
                        return render(request, "ForgetPassword.html", {"form": form, "result": result})
                else:
                    result = "两次输入的密码不同"
                    return render(request, "ForgetPassword.html", {"form": form, "result": result})
            else:
                result = "密保问题答案错误"
                return render(request, "ForgetPassword.html", {"form": form, "result": result})
        else:
            result = "用户不存在"
            return render(request, "ForgetPassword.html", {"form": form, "result": result})
    else:
        form = ForgetPasswordForm()
        return render(request, "ForgetPassword.html", {"form": form})
