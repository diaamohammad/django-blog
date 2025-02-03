from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

app_name = 'blog'

urlpatterns = [
    
    path('signup/',views.SiginUpView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name="blog/registeration/login.html", next_page="/blog/"), name='login'),
    path('',views.PostListView.as_view(),name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>',views.post_detial,name='post_detial'),
    path('<int:post_id>/comment/',views.comment_post,name='post_comment')
    

]