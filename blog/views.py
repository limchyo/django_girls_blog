from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Comment
from .forms import PostForm, CommentForm

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

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now()
            post.save()
            return redirect("post_detail", post.id) #post_detail URL에서 id값 먹인 곳

    else:
        form = PostForm() # 기본 폼은 비어있으므로 저장 실패시 빈 폼

    ctx = { "form" : form }
    return render(request, "post_edit.html", ctx)

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, id=pk) # 객체가 없는 경우 404 처리
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now()
            post.save()
            return redirect("post_detail", post.id)
    else:
        form = PostForm(instance=post)

    ctx = { "form" : form }
    return render(request, "post_edit.html", ctx)

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    ctx = { "posts" : posts}
    return render(request, 'post_draft_list.html', ctx)

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, id=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, id=pk)
    post.delete()
    return redirect('post_list')

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'add_comment_to_post.html', {'form': form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)
