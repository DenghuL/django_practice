"""MyForum URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    to_know_more_info.py. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    to_know_more_info.py. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    to_know_more_info.py. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, re_path
# from ..boards.views import PostUpDataView
from boards import views as boards_views
from accounts import views as account_views
urlpatterns = [
    path('admin/', admin.site.urls),

    path('home/', boards_views.BoardListView.as_view(), name="home", ),
    path('', boards_views.BoardListView.as_view(), name="/", ),
    # 使用正则表达式的时候，使用re_path来路由，其中:?P<pk>表示后面表达式（\d+）匹配的值传入pk中
    re_path(r"^boards/(?P<pk>\d+)/$", boards_views.TopicListView.as_view(), name='board_topics'),
    re_path(r"^boards/(?P<pk>\d+)/new/$", boards_views.new_topic, name='new_topic'),

    path('signup/', account_views.signup, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),

    # 密码重置的过程，4个过程
    re_path(r'^reset/$',
            auth_views.PasswordResetView.as_view(
                template_name='password_reset.html',
                email_template_name='password_reset_email.html',
                subject_template_name='password_reset_subject.txt'),
            name='password_reset'),
    re_path(r'^reset/done/$',
            auth_views.PasswordResetDoneView.as_view(
                template_name='password_reset_done.html'),
            name='password_reset_done'),
    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            auth_views.PasswordResetConfirmView.as_view(
                template_name='password_reset_confirm.html'),
            name='password_reset_confirm'),
    re_path(r'^reset/complete/$',
            auth_views.PasswordResetCompleteView.as_view(
                template_name='password_reset_complete.html'),
            name='password_reset_complete'),
    re_path(r'^settings/password/$',
            auth_views.PasswordChangeView.as_view(
                template_name='password_change.html'),
            name='password_change'),
    re_path(r'^settings/password/done/$',
            auth_views.PasswordChangeDoneView.as_view(
                template_name='password_change_done.html'),
            name='password_change_done'),


    re_path(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/reply/$', boards_views.reply_topic, name='reply_topic'),
    re_path(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/$', boards_views.PostListView.as_view(), name='topic_posts'),
    re_path(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/posts/(?P<post_pk>\d+)/edit/$',
            boards_views.PostUpDataView.as_view(),
            name='edit_post'),
    re_path(r'^settings/account/$', account_views.UserUpdateView.as_view(), name='my_account'),
    ]
