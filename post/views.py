from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Image
from .forms import PostForm

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
    context={
        'post':post,
        'images':images,
    }
    return render(request, 'detail.html', context)
    
# form = []
#     for post in posts:
#         image = Image.objects.filter(post=post).first()
#         form.append(post, image)