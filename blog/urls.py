from django.urls import path
from . import views as blog_view
from . import api as api_view
app_name = 'blog'

urlpatterns = [
    path('', blog_view.PostListView.as_view(), name='home'),
    path('post/user/<str:username>/', blog_view.UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', blog_view.PostDetailView.as_view(), name='post-detail'),
    path('post/new/', blog_view.PostCreateView.as_view(), name='post-create'),
    path('post/update/<int:pk>/', blog_view.PostUpdateView.as_view(), name='post-update'),
    path('post/delete/<int:pk>/', blog_view.PostDeleteView.as_view(), name='post-delete'),
    path('api/posts/', api_view.post_list_api, name='post_list_api'),
    path('api/posts/<int:id>', api_view.post_detail_api, name='post_detail_api'),
    path('api/comments/', api_view.comment_list_api, name='comment_list_api'),
    path('api/comments/<int:id>', api_view.comment_detail_api, name='comment_detail_api'),
]