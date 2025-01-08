from django.shortcuts import render

# Create your views here.
def music_homepage_rendering_views(request):  # 渲染主页面为music_home_page.html
    return render(request, 'music_home_page.html')