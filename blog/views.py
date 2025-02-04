from django.shortcuts import render,get_object_or_404,redirect
from .models import Post,Comment
from django.http import Http404
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.views.generic import ListView,CreateView
from .forms import CommentForm
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


class SiginUpView(CreateView):
    
    form_class = UserCreationForm
    success_url = reverse_lazy('blog:login')
    template_name = 'blog/registeration/signup.html'

    def form_valid(self, form):
        form.save()

        return redirect(self.success_url)
    
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
    
def profile_view(request):
    return render(request,'profile.html')

class PostListView(LoginRequiredMixin, ListView):

    model = Post
    context_object_name = 'posts'
    paginate_by = 2
    template_name = 'blog/post/list.html'
    login_url = 'login/'
    redirect_field_name = 'next'


@login_required(login_url='login/')   
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


@login_required(login_url='login/')
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
