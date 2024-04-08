from .views import PostList, PostDetail, PostListAPI, PostDetailAPI, genericApi #genericListApi, genericDetailApi#
from django.urls import path


urlpatterns = [
    # path("posts/", PostList),
    # path("posts/<int:pk>", PostDetail),
    
    # path("posts/", PostListAPI.as_view()),
    # path("posts/<int:pk>", PostDetailAPI.as_view()),
    
    path("posts/", genericApi.as_view(), name="posts"),
    path("posts/<int:id>", genericApi.as_view(), name="post"),
]
