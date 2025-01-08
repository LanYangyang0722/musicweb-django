from django.shortcuts import render,redirect
from index.models import user_schedule
from index.models import admin_schedule
# Create your views here.

from index.models import song_schedule

from django.db.models import Q















#**************************************实现用户注册功能***************************************#
def user_register_views(request):  # 注册功能
    u = request.POST.get("user", '')
    p = request.POST.get("pwd", '')
    p1 = request.POST.get("pwd1", '')
    m = request.POST.get("mail", '')

    # 检查用户名或邮箱是否为空
    if not u or not p or not m or not p1:
        return render(request, "music_home_page.html", {"error": "请输入完整的信息!"})
    # 检查密码是否一致
    if p != p1:
        return render(request, "music_home_page.html", {"error": "两次密码不一致!"})
    # 检查用户名是否已存在
    if user_schedule.objects.filter(user_name=u).exists():
        return render(request, "music_home_page.html", {"error": "用户名已存在!"})
    # 检查邮箱是否已存在
    if user_schedule.objects.filter(user_email=m).exists():
        return render(request, "music_home_page.html", {"error": "邮箱已被注册!"})
    # 如果通过所有检查，保存用户信息
    ug = user_schedule(user_name=u, user_password=p, user_email=m)
    ug.save()
    return render(request, "music_home_page.html", {"success": "注册成功！"})



#**************************************#用户页面视图渲染***************************************#
def user_home_page_redering_views(request, user_id):
    try:
        user = user_schedule.objects.get(user_id=user_id)  # 使用 user_id
    except user_schedule.DoesNotExist:
        return render(request, 'music_home_page.html', {"error": "用户不存在!"})

    return render(request, 'user_home_page.html', {"user": user})  # 将用户信息传递给用户主页


#**************************************#实现用户登录功能***************************************#
def user_login_views(request):
    if request.method == "POST":
        u = request.POST.get("user", '')
        p = request.POST.get("pwd", '')

        # 检查用户输入的用户名和密码是否正确
        user = user_schedule.objects.filter(user_name=u).first()  # 查找用户名对应的用户
        if user and user.user_password == p:  # 密码匹配
            # 登录成功，重定向到用户主页，并传递用户 ID
            return redirect('user_home_page', user_id=user.user_id)#不能直接访问html

        else:
            # 登录失败，返回错误信息
            return render(request, 'music_home_page.html', {"login_failed1": True})

    return render(request, 'music_home_page.html')  # GET 请求时，返回登录页面


def user_search_songs(request, user_id):
    # 获取搜索关键词
    search_query = request.GET.get('search', '')
    user = user_schedule.objects.get(user_id=user_id)

    # 如果搜索关键词不为空，进行搜索
    if search_query:
        # 使用 Q 对象进行模糊匹配，同时匹配歌曲名和歌手名
        songs = song_schedule.objects.filter(
            Q(song_name__icontains=search_query) | Q(singer_name__icontains=search_query)
        )
    else:
        songs = song_schedule.objects.all()  # 如果没有搜索条件，返回所有歌曲

    # 获取当前播放的歌曲路径（如果有的话），如果没有，默认为空
    current_song_path = request.GET.get('current_song_path', '')

    return render(request, 'user_home_page.html', {
        'user': user,
        'songs': songs,
        'search_query': search_query,
        'current_song_path': current_song_path,  # 传递当前歌曲路径
    })