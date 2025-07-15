from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category
from .forms import CommentForm
from django.contrib import messages

def post_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    posts = Post.objects.filter(status='published')  # Только опубликованные статьи
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        posts = posts.filter(category=category)
    return render(request, 'blog/post_list.html', {'posts': posts, 'categories': categories, 'category': category})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    comments = post.comments.filter(active=True)  # Только активные комментарии
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Создать объект comment, но пока не сохранять в базе данных
            new_comment = comment_form.save(commit=False)
            # Привязать comment к текущей статье
            new_comment.post = post
            # Сохранить comment в базе данных
            new_comment.save()
            messages.success(request, 'Comment added successfully!')
            return redirect(request.path) # Перезагружаем страницу для отображения нового комментария
        else:
            messages.error(request, 'Error adding comment.')
    else:
        comment_form = CommentForm()
    return render(request, 'blog/post_detail.html',
                  {'post': post,
                   'comments': comments,
                   'new_comment': new_comment,
                   'comment_form': comment_form})