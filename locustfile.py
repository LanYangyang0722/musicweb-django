from locust import HttpUser, task, between

class MusicHomePageUser(HttpUser):
    # 用户间的间隔时间，模拟不同用户之间的操作间隔
    wait_time = between(1, 3)  # 每个用户请求后等待 1 到 3 秒之间

    @task
    def load_homepage(self):
        # 访问 Django 视图渲染的主页
        self.client.get('/')  # 假设这个 URL 对应你定义的视图
