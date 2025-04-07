from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Image, Comment
from .forms import PostForm
from django.utils import timezone


# Create your views here.
def list_view(request):
    posts=Post.objects.all()
    return render(request, 'list.html', {'posts' : posts})

def write_veiw(request):
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
    
def detail_veiw(request, post_id):
    post=get_object_or_404(Post, pk=post_id)
    images=Image.objects.filter(post=post)
    comments=Comment.objects.filter(post=post)
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