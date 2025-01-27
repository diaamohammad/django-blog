from . import views
from django.urls import path
app_name = 'blog'

urlpatterns = [
    #path('',views.post_list,name='post_list'),
    path('',views.PostListView.as_view(),name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>',views.post_detial,name='post_detial'),
    path('<int:post_id>/comment/',views.comment_post,name='post_comment')
    

]