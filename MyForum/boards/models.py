import math

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
from django.utils.text import Truncator
from django.utils.html import mark_safe
from markdown import markdown

class Board(models.Model):
    """
    板块，主要用于首页的版面分类
    管理员可以创建板块
     字段：
        name（唯一）
        description
    """
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_posts_count(self):
        return Post.objects.filter(topic__board=self).count()

    def get_last_post(self):
        return Post.objects.filter(topic__board=self).order_by('-created_at').first()


class Topic(models.Model):
    """
    subject:表示主题内容，
    last_update: 用来定义话题的排序，
    starter: 用来识别谁发起的话题，
    board:用于指定它属于哪个版块。
    """
    subject = models.CharField(max_length=250)
    last_update = models.DateTimeField(auto_now=True)
    starter = models.ForeignKey(User, on_delete=models.CASCADE,related_name='topics')
    board = models.ForeignKey(Board, on_delete=models.CASCADE,related_name='topics')
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.subject

    def get_page_count(self):
        count = self.posts.count()
        pages = count / 20
        return math.ceil(pages)

    def has_many_pages(self, count=None):
        if count is None:
            count = self.get_page_count()
        return count > 6

    def get_page_range(self):
        count = self.get_page_count()
        if self.has_many_pages(count):
            return range(1, 5)
        return range(1, count + 2)

    def get_last_ten_posts(self):
        return self.posts.order_by('-created_at')[:10]

class Post(models.Model):
    """
    message 字段，用于存储回复的内容，
    created_at 在排序时候用（最先发表的帖子排最前面），
    updated_at 告诉用户是否更新了内容，
    同时，还需要有对应的 User 模型的引用，Post 由谁创建的和谁更新的。
    """
    message = models.TextField(max_length=4000)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE,related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name='posts')
    updated_by = models.ForeignKey(User,on_delete=models.CASCADE, null=True, related_name='+')

    def __str__(self):
        truncated_message = Truncator(self.message)
        return truncated_message.chars(30)

    def get_message_as_markdown(self):
        return mark_safe(markdown(self.message, safe_mode='escape'))

