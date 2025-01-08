from django.test import TestCase
from django.urls import reverse


class MusicHomepageTestCase(TestCase):
    def test_music_homepage_renders_correct_template(self):
        # 使用 reverse() 来获得视图的URL，reverse函数根据视图的名称自动生成URL
        url = '/'

        # 发起 GET 请求，模拟用户访问主页
        response = self.client.get(url)

        # 确认响应状态码是200，表示请求成功
        self.assertEqual(response.status_code, 200)

        # 确认响应中使用了正确的模板（即 music_home_page.html）
        self.assertTemplateUsed(response, 'music_home_page.html')
