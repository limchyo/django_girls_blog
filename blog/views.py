from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm

# Create your views here.
def post_list(request):
    ctx = {}
    post = Post.objects.all()
    post = post.filter(published_date__lte=timezone.now())
    post = post.order_by('published_date')

    ctx.update({ "post" : post })
    return render(request, "post_list.html", ctx)

def post_detail(request, pk):
    ctx = {}
    post = get_object_or_404(Post, id=pk) # 객체가 없는 경우 404 처리
    # post = Post.objects.get(id=pk)
    ctx.update({ "post" : post })
    return render(request, "post_detail.html", ctx)

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect("post_detail", post.id) #post_detail URL에서 id값 먹인 곳

    else:
        form = PostForm() # 기본 폼은 비어있으므로 저장 실패시 빈 폼

    ctx = { "form" : form }
    return render(request, "post_edit.html", ctx)

def post_edit(request, pk):
    post = get_object_or_404(Post, id=pk) # 객체가 없는 경우 404 처리
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect("post_detail", post.id)
    else:
        form = PostForm(instance=post)
        
    ctx = { "form" : form }
    return render(request, "post_edit.html", ctx)
