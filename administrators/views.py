from django.shortcuts import render, redirect
from index.models import user_schedule, admin_schedule
from django.shortcuts import get_object_or_404
from index.models import song_schedule
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from index.models import singer_schedule
import os
# 渲染管理员页面
def administrators_home_page_rendering_views(request):
    return render(request, 'administrators_home_page.html')

# 渲染管理员登录页面
def administrators_login_page_rendering_views(request):
    return render(request, 'administrators_login_page.html')

# 渲染管理用户页面
def administrators_usermanage_page_rendering_views(request):
    search_query = request.GET.get('search', '')
    users = user_schedule.objects.all()  # 默认查询所有用户

    if search_query:
        # 通过用户名或邮箱查找匹配的用户
        users = users.filter(user_name__icontains=search_query) | users.filter(user_email__icontains=search_query)

    return render(request, 'administrators_usermanage_page.html', {'users': users, 'search_query': search_query})

# 渲染管理歌曲页面


# 管理员登录功能
def administrators_login_views(request):
    u = request.POST.get("user", "")
    p = request.POST.get("pwd", "")
    if u and p:
        c = admin_schedule.objects.filter(admin_name=u, admin_password=p).count()
        if c >= 1:
            return redirect('administrators_home_page')  # 跳转到 admin_page 页面
        else:
            return render(request, "administrators_login_page.html", {"login_failed1": True})
    else:
        return render(request, "administrators_login_page.html", {"login_failed": True})



def edit_user(request, user_id):
    user = get_object_or_404(user_schedule, user_id=user_id)

    if request.method == 'POST':
        # 获取用户提交的表单数据
        user_name = request.POST.get('user_name', '')
        user_password = request.POST.get('user_password', '')
        user_email = request.POST.get('user_email', '')

        # 查重：检查用户名和邮箱是否已存在
        if user_name != user.user_name and user_schedule.objects.filter(user_name=user_name).exists():
            messages.error(request, "用户名已存在，请选择其他用户名。")
            return render(request, 'edit_user.html', {'user': user})

        if user_email != user.user_email and user_schedule.objects.filter(user_email=user_email).exists():
            messages.error(request, "邮箱已存在，请选择其他邮箱。")
            return render(request, 'edit_user.html', {'user': user})

        # 更新用户信息
        if user_name:
            user.user_name = user_name
        if user_password:
            user.user_password = user_password
        if user_email:
            user.user_email = user_email

        # 保存修改
        user.save()
        return redirect('administrators_usermanage_page')  # 修改后重定向回管理页面

    return render(request, 'edit_user.html', {'user': user})




def administrators_songsmanage_page_rendering_views(request):
    search_query = request.GET.get('search', '')
    songs = song_schedule.objects.all()  # 默认查询所有歌曲

    # 搜索功能：按歌曲名称进行过滤
    if search_query:
        songs = songs.filter(song_name__icontains=search_query)

    # 处理文件上传
    if request.method == 'POST' and request.FILES:
        song_name = request.POST.get('song_name', '')
        singer_name = request.POST.get('singer_name', '')
        song_category = request.POST.get('song_category', '')
        song_file = request.FILES.get('song_file')
        song_image = request.FILES.get('song_image')

        if not song_name or not singer_name or not song_file:
            messages.error(request, "所有字段都是必填的，包括歌曲文件和歌曲图片。")
            return render(request, 'administrators_songsmanage_page.html', {'songs': songs})

        # 使用相对路径保存 MP3 文件
        fs = FileSystemStorage(location=settings.MEDIA_ROOT)  # 使用 MEDIA_ROOT
        song_file_path = fs.save(f'songs/video/{song_file.name}', song_file)

        # 保存图片文件
        song_image_path = None
        if song_image:
            song_image_path = fs.save(f'songs/img/{song_image.name}', song_image)

        # 创建新的歌曲记录
        song_schedule.objects.create(
            song_name=song_name,
            singer_name=singer_name,
            song_category=song_category,
            song_file_path=f'songs/video/{song_file.name}',
            song_image_path=f'songs/img/{song_image.name}' if song_image else None,
        )

        messages.success(request, "歌曲上传成功！")
        return redirect('administrators_songsmanage_page')  # 上传完成后重定向回歌曲管理页面

    return render(request, 'administrators_songsmanage_page.html', {'songs': songs, 'search_query': search_query})


# 删除歌曲
def delete_song(request, song_id):
    # 获取要删除的歌曲
    song = get_object_or_404(song_schedule, song_id=song_id)

    # 删除歌曲文件和图片
    if song.song_file_path:
        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        fs.delete(song.song_file_path)

    if song.song_image_path:
        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        fs.delete(song.song_image_path)

    # 删除歌曲记录
    song.delete()

    # 显示删除成功的消息
    messages.success(request, "歌曲删除成功！")

    # 删除后重定向回歌曲管理页面
    return redirect('administrators_songsmanage_page')
def delete_user(request, user_id):
    # 获取要删除的用户
    user = get_object_or_404(user_schedule, user_id=user_id)

    # 删除用户
    user.delete()

    # 显示删除成功的消息
    messages.success(request, "用户删除成功！")

    # 删除后重定向回用户管理页面
    return redirect('administrators_usermanage_page')




#**************************************歌手管理************************#

def administrators_singersmanage_page_rendering_views(request):
    singers = singer_schedule.objects.all()
    if 'search' in request.GET:
        search_query = request.GET['search']
        singers = singers.filter(singer_name__icontains=search_query)
    return render(request, 'administrators_singersmanage_page.html', {'singers': singers})


def add_singer(request):
    if request.method == 'POST':
        singer_name = request.POST['singer_name']
        singer_bio = request.POST['singer_bio']

        # 处理图片上传
        singer_image = request.FILES.get('singer_image')
        if singer_image:
            fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'singer'))
            singer_image_path = fs.save(singer_image.name, singer_image)
        else:
            singer_image_path = ''

        # 创建歌手记录
        singer_schedule.objects.create(
            singer_name=singer_name,
            singer_bio=singer_bio,
            singer_image_path=singer_image_path
        )
        messages.success(request, "歌手信息添加成功！")
        return redirect('administrators_singersmanage_page')

    return render(request, 'add_singer.html')


def edit_singer(request, singer_id):
    singer = get_object_or_404(singer_schedule, pk=singer_id)

    if request.method == 'POST':
        singer_name = request.POST['singer_name']
        singer_bio = request.POST['singer_bio']

        # 处理图片上传
        singer_image = request.FILES.get('singer_image')
        if singer_image:
            fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'singer'))
            singer_image_path = fs.save(singer_image.name, singer_image)
            # 删除旧图片
            if singer.singer_image_path:
                fs.delete(singer.singer_image_path)
        else:
            singer_image_path = singer.singer_image_path

        # 更新歌手信息
        singer.singer_name = singer_name
        singer.singer_bio = singer_bio
        singer.singer_image_path = singer_image_path
        singer.save()

        messages.success(request, "歌手信息更新成功！")
        return redirect('administrators_singersmanage_page')

    return render(request, 'edit_singer.html', {'singer': singer})






def delete_singer(request, singer_id):
    singer = get_object_or_404(singer_schedule, pk=singer_id)

    # 删除歌手图片
    if singer.singer_image_path:
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'singer'))
        fs.delete(singer.singer_image_path)

    # 删除歌手记录
    singer.delete()

    messages.success(request, "歌手信息删除成功！")
    return redirect('administrators_singersmanage_page')






















