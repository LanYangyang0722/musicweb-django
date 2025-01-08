from django.db import models

# Create your models here.
class user_schedule(models.Model):
    user_id = models.AutoField(primary_key=True)  # 自增主键，用户ID
    user_name = models.CharField(max_length=255, unique=True)  # 用户名，唯一
    user_password = models.CharField(max_length=255)  # 密码
    user_email = models.CharField(max_length=255, unique=True)  # 邮箱，唯一

    def __str__(self):
        return self.user_id  # 返回用户名，便于调试和显示

# 管理员表
class admin_schedule(models.Model):
    admin_id = models.AutoField(primary_key=True)  # 自增主键，管理员ID
    admin_name = models.CharField(max_length=255, unique=True)  # 管理员用户名，唯一
    admin_password = models.CharField(max_length=255)  # 管理员密码

    def __str__(self):
        return self.admin_id  # 返回管理员用户名，便于调试和显示


class song_schedule(models.Model):
    song_id = models.AutoField(primary_key=True)  # 自增主键，歌曲ID
    song_name = models.CharField(max_length=255)  # 歌曲名字，可以重复
    singer_name = models.CharField(max_length=255)  # 歌手名字，可以重复
    song_image_path = models.CharField(max_length=255, blank=True, null=True)  # 歌曲图片保存路径
    song_file_path = models.CharField(max_length=255)  # 歌曲文件保存路径
    song_category = models.CharField(max_length=255, blank=True, null=True)  # 歌曲分类（如：流行、摇滚等）

    def __str__(self):
        return str(self.song_id)  # 返回歌曲ID，便于调试和显示



class singer_schedule(models.Model):
    singer_id = models.AutoField(primary_key=True)  # 自增主键，歌手ID
    singer_name = models.CharField(max_length=255, unique=True)  # 歌手名字，唯一
    singer_bio = models.TextField(blank=True, null=True)  # 歌手简介，可为空
    singer_image_path = models.CharField(max_length=255, blank=True, null=True)  # 歌手图片保存路径

    def __str__(self):
        return self.singer_id  # 返回歌手id，便于调试和显示