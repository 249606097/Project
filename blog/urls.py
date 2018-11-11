from django.conf.urls import url, include
from blog import views


urlpatterns = [
    url(r'^register', views.register, name='register'),
    url(r'^login', views.login, name='login'),
    url(r'^change_password', views.change_password, name='change_password'),
    url(r'^forget_password', views.forget_password, name='forget_password'),
    url(r'^write', views.write, name='write'),
    url(r'^comment/(?P<id>\d+)/', views.to_comment, name='comment'),
    url(r'^article_list', views.article_list, name='article_list'),
    url(r'^article/(?P<id>\d+)/', views.article_page, name='article_page'),
    url(r'^edit_article/(?P<id>\d+)/', views.edit_article, name='edit_article'),
    url(r'^delete_article/(?P<id>\d+)/', views.delete_article, name='delete_article'),
    url(r'^un_login', views.to_delete_cookie, name="logout"),


    url(r'^', views.welcome_page, name='welcome'),
]
