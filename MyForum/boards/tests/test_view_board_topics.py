from django.test import TestCase
from django.urls import reverse, resolve


from ..views import board_topics
from ..models import Board


class BoardTopicsTests(TestCase):
    def setUp(self):
        """
        创建一个Board实例来进行测试
        :return:
        """
        Board.objects.create(name='Django', description='Django board.')

    def test_board_topics_view_success_staus_code(self):
        """
        测试访问 board_topics 页面返回：200
        :return:
        """
        path = reverse('board_topics', kwargs={"pk": 1})
        response = self.client.get(path)
        self.assertEquals(response.status_code, 200)

    def test_board_topics_view_not_found_staus_code(self):
        """
        访问失败时的页面提示：404
        :return:
        """
        path = reverse("board_topics", kwargs={"pk": 99})
        response = self.client.get(path)
        self.assertEquals(response.status_code, 404)

    def test_board_url_resolves_board_topics_view(self):
        view = resolve("/boards/1/")
        self.assertEquals(view.func, board_topics)


    def test_board_topics_view_contains_link_back_to_homepage(self):
        """
        测试从主题返回首页的链接
        """
        board_topics_url=reverse("board_topics",kwargs={"pk":1})  # 获取路由
        response = self.client.get(board_topics_url)  # 请求 topic 接口
        homepage_url = reverse('home')  # 获取 home 的路由
        self.assertContains(response, f'href="{homepage_url}"')

    def test_board_topics_view_contains_navigation_links(self):
        board_topics_url = reverse('board_topics', kwargs={'pk': 1})
        homepage_url = reverse('home')
        new_topic_url = reverse('new_topic', kwargs={'pk': 1})

        response = self.client.get(board_topics_url)

        self.assertContains(response, 'href="{0}"'.format(homepage_url))
        self.assertContains(response, 'href="{0}"'.format(new_topic_url))