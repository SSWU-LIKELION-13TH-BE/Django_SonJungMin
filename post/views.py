from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Image, Comment
from .forms import PostForm
from django.utils import timezone
from django.urls import reverse
from django.db.models import Q, Count
from django.core.paginator import Paginator

# Create your views here.
def list_view(request):
    sort = request.GET.get('list_sort', '')
    if sort == 'popular':
        posts = Post.objects.all().annotate(like_count=Count('likes')).order_by('-like_count','-created_at')
    else:
        posts = Post.objects.all().order_by('-created_at')
    return render(request, 'list.html', {'posts' : posts})

def write_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            
            for img in request.FILES.getlist('image', None):
                Image.objects.create(post=post, image=img)
                
            return redirect('post:list')
        return redirect('post:write')
    else:
        form=PostForm()
        return render(request, 'write.html', {'form':form})
    
def detail_view(request, post_id):
    post=get_object_or_404(Post, pk=post_id)
    images=Image.objects.filter(post=post)
    comments=Comment.objects.filter(post=post)
    post.views+=1
    post.save()
    context={
        'post':post,
        'images':images,
        'comments':comments,
    }
    return render(request, 'detail.html', context)
    
def comment_view(request, post_id):
    post = Post.objects.get(pk=post_id)
    if request.method == 'POST':
        comment_content = request.POST['comments']
        parent_comment_id = request.POST.get('parent_comment_id')  
        
        if parent_comment_id:
            parent_comment = Comment.objects.get(pk=parent_comment_id)
            new_comment = Comment(post=post, parent_comment=parent_comment, comment_content=comment_content, comment_datetime=timezone.now(), user=request.user)
        else:
            new_comment = Comment(post=post, comment_content=comment_content, comment_datetime=timezone.now(), user=request.user)
        
        new_comment.save() 
        
        return redirect('post:detail', post_id=post_id)
    
    return redirect('post:detail', post_id=post_id)

def post_likes_view(request, post_id):
    post = Post.objects.get(pk=post_id)
    if request.user.is_authenticated:
        if post.likes.filter(pk=request.user.pk).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        return redirect('post:detail', post_id)
    return redirect('user:login')

def comment_likes_view(request, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    if request.user.is_authenticated:
        post_id=comment.post.id
        if comment.likes.filter(pk=request.user.pk).exists():
            comment.likes.remove(request.user)
        else:
            comment.likes.add(request.user)
        return redirect('post:detail', post_id )
    return redirect('user:login')

def search_view(request):
    searchbar=request.GET.get('searchbar','')
    search_terms=set(searchbar.replace(',',' ').split())
    search_terms=set(term.lower() for term in search_terms)
    
    query=Q()
    
    for term in search_terms:
        query |= Q(title__icontains = term)
    
    posts=Post.objects.filter(query)

    post_with_count = []
    
    for post in posts:
        count = sum(post.title.count(term) for term in search_terms)
        # images = Image.objects.filter(post_id=post.id)
        
        post_with_count.append((post, count))
            
    post_with_count.sort(key = lambda x:(x[1], x[0].created_at), reverse=True)
    sorted_posts=[post for post, count in post_with_count]
        
    return render(request, 'search.html', {'posts':sorted_posts})
    
        