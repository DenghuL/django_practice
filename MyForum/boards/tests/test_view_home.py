from django.test import TestCase
from django.urls import reverse, resolve
from ..views import home
from ..models import Board


class HomeTests(TestCase):

    def setUp(self):
        """
        创建一个Board实例来进行测试
        :return:
        """
        self.board = Board.objects.create(name='Django', description='Django board.')
        path = reverse('home')  # 需要在urls中添加一个name="home"，方可不报错
        self.response = self.client.get(path)

    def test_home_view_status_code(self):
        """
        测试访问 home 页面状态码为 200
        :return:
        """
        self.assertEquals(self.response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        """
        测试路由： ”/“ 返回为首页函数
        :return:
        """
        view = resolve('/')
        self.assertEquals(view.func, home)

    def test_home_view_contains_link_topics_page(self):
        """
        测试主页中是否有 topics_page导航链接
        测试主题返回主体中是否包含 href="/boards/to_know_more_info.py/"
        :return:
        """
        board_topics_url = reverse("board_topics", kwargs={"pk": self.board.pk})
        self.assertContains(self.response, f'href="{board_topics_url}"')
