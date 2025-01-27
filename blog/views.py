from django.shortcuts import render,get_object_or_404
from .models import Post,Comment
from django.http import Http404
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.views.generic import ListView,CreateView
from .forms import CommentForm
from django.views.decorators.http import require_POST


#def post_list(request):
   # post_list = Post.objects.all()
   # paginator = Paginator(post_list,2)
   # page_number = request.GET.get('page',1)

   # try:
     #   posts = paginator.page(page_number)
   # except PageNotAnInteger:
    #    posts = paginator.page(1)
    #except EmptyPage:
        #posts = paginator.page(page_number.num_pages)
    #return render(request,'blog/post/list.html',{'posts':posts})

class PostListView(ListView):

    model = Post
    context_object_name = 'posts'
    paginate_by = 2
    template_name = 'blog/post/list.html'
    
def post_detial(request,year,month,day,post):

    post = get_object_or_404(Post, status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,
                             
                             )
    comments= post.comments.filter(active=True)
    form = CommentForm()
    return render(request,'blog/post/detial.html',{'post':post,'comments':comments, 'form':form})

@require_POST
def comment_post(request,post_id):

    post = get_object_or_404(Post,id=post_id,status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    
    
    return render(request,'blog/post/comment.html',{'form':form, 'post':post, 'comment':comment})
