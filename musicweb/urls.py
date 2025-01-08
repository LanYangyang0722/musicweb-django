from django.contrib import admin
from django.urls import path
from index import views as index_views
from administrators import views as admin_views
from user_model import views as user_views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    # 主页面路径 — 渲染主页面函数
    # 修改主页面路径，给它设置一个名称
    path('', index_views.music_homepage_rendering_views, name='music_homepage'),

    # 用户注册功能
    path('user_register/', user_views.user_register_views),

    # 用户页面路径（动态 URL 和用户主页相关）
    path('user_page/<int:user_id>/', user_views.user_home_page_redering_views, name='user_home_page'),  # 用户主页, 动态 URL

    # 用户登录功能
    path('user_login/', user_views.user_login_views),

    # 管理员登录页面路径 — 渲染管理员登录页面函数
    path('administrators_login_page/', admin_views.administrators_login_page_rendering_views),

    # 管理员页面路径 — 渲染管理员页面函数
    path('administrators_home_page/', admin_views.administrators_home_page_rendering_views, name='administrators_home_page'),

    # 管理员登录功能 — 管理员登录函数
    path('administrators_login/', admin_views.administrators_login_views),

    # 管理员用户页面路径 — 渲染管理用户页面函数
    path('administrators_usermanage_page/', admin_views.administrators_usermanage_page_rendering_views, name='administrators_usermanage_page'),

    # 管理员歌曲页面路径 — 渲染管理歌曲页面函数


    path('administrators_usermanage_page/', admin_views.administrators_usermanage_page_rendering_views,name='administrators_usermanage_page'),

    # 编辑用户页面
    path('edit_user/<int:user_id>/', admin_views.edit_user, name='edit_user'),

    path('administrators_songsmanage_page/', admin_views.administrators_songsmanage_page_rendering_views, name='administrators_songsmanage_page'),

    path('delete_song/<int:song_id>/', admin_views.delete_song, name='delete_song'),

    path('delete_user/<int:user_id>/', admin_views.delete_user, name='delete_user'),



    path('administrators_singersmanage_page/', admin_views.administrators_singersmanage_page_rendering_views,name='administrators_singersmanage_page'),
    path('add_singer/', admin_views.add_singer, name='add_singer'),
    path('edit_singer/<int:singer_id>/', admin_views.edit_singer, name='edit_singer'),



    path('delete_singer/<int:singer_id>/', admin_views.delete_singer, name='delete_singer'),

    path('user_search_songs/<int:user_id>/', user_views.user_search_songs, name='user_search_songs'),





]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)