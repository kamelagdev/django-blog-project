from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer


@api_view(['GET'])
def post_list_api(request):
    posts = Post.objects.all()
    data = PostSerializer(posts, many=True).data
    return Response(data)


@api_view(['GET'])
def post_detail_api(request, id):
    post = Post.objects.get(id=id)
    data = PostSerializer(post).data
    return Response(data)


@api_view(['GET'])
def comment_list_api(request):
    comments = Comment.objects.all()
    data = CommentSerializer(comments, many=True).data
    return Response(data)


@api_view(['GET'])
def comment_detail_api(request, id):
    comment = get_object_or_404(Comment, id=id)
    data = CommentSerializer(comment).data
    return Response(data)
