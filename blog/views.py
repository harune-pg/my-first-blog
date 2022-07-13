from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

# URLが'post/new/'の場合に呼び出される
def post_new(request):
    # Saveボタンでフォームを送信して同じビューに戻される場合('post_edit.html'読み込み後はmethodがPOSTになっている)
    if request.method == "POST":
        # フォームデータをもとにインスタンスを生成する
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)  # postをPostに保存する前にauthorを追加したいので、'commit=False'で保存を拒否する
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    # 最初にページにアクセスしてきた場合
    else:
        # PostForm()でフォームを新規作成して表示させる
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)  # 引数はアクセスしたいレコードの情報
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)  # 第一引数はPOSTデータを使用するため、第二引数は既存のpostを編集するためにある
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})