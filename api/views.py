from django.shortcuts import render
from .models import Post
from .serializers import PostSerializer

# from django.http import JsonResponse
# from rest_framework.parsers import JSONParser
# from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Classed based views
from rest_framework.views import APIView
from django.http import Http404

# Generic views
from rest_framework import generics
from rest_framework import mixins

# Viewsets
from rest_framework import viewsets
from django.shortcuts import get_object_or_404


# Authentication and permissions

from rest_framework import viewsets
from rest_framework.authentication import (
    SessionAuthentication,
    BasicAuthentication,
    TokenAuthentication,
)
from rest_framework.permissions import IsAuthenticated


# Create your views here.

class PostViewSet(viewsets.ViewSet):
    def list(self, request):
        posts = Post.objects.all()
        postSerializer = PostSerializer(posts, many=True)
        return Response(postSerializer.data)

    def create(self, request):
        postSerializer = PostSerializer(data=request.data)

        if postSerializer.is_valid():
            postSerializer.save()
            return Response(postSerializer.data, status=status.HTTP_201_CREATED)
        return Response(postSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = Post.objects.all()
        post = get_object_or_404(queryset, pk=pk)
        postSerializer = PostSerializer(post)
        return Response(postSerializer.data)

    def update(self, request, pk=None):
        post = Post.objects.get(pk=pk)
        postSerializer = PostSerializer(post, data=request.data)

        if postSerializer.is_valid():
            postSerializer.save()
            return Response(postSerializer.data)
        return Response(postSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        post = Post.objects.get(pk=pk)
        post.delete()
        return Response({"message": "Post was deleted successfully!"})
    
    


class genericApi(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    lookup_field = "id"

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        if id:
            return self.retrieve(request)
        else:
            return self.list(request)

    def post(self, request):
        return self.create(request)

    def put(self, request, id=None):
        return self.update(request, id)

    def delete(self, request, id=None):
        return self.destroy(request, id)


# class genericListApi (mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView, mixins.RetrieveModelMixin):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


# class genericDetailApi (mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)


###################################################
class PostListAPI(APIView):
    def get(self, request):
        posts = Post.objects.all()
        postSerializer = PostSerializer(posts, many=True)
        return Response(postSerializer.data)

    def post(self, request):
        postSerializer = PostSerializer(data=request.data)

        if postSerializer.is_valid():
            postSerializer.save()
            return Response(postSerializer.data, status=status.HTTP_201_CREATED)
        return Response(postSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailAPI(APIView):
    def get(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)

        except Post.DoesNotExist:
            return Response(
                {"message": "The post does not exist"}, status=status.HTTP_404_NOT_FOUND
            )

        postSerializer = PostSerializer(post)
        return Response(postSerializer.data)

    def put(self, request, pk):
        post = Post.objects.get(pk=pk)
        postSerializer = PostSerializer(post, data=request.data)

        if postSerializer.is_valid():
            postSerializer.save()
            return Response(postSerializer.data)
        return Response(postSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.delete()

        return Response({"message": "Post was deleted successfully!"})


######################################""


@api_view(["GET", "POST"])
def PostList(request):

    if request.method == "GET":
        posts = Post.objects.all()
        postSerializer = PostSerializer(posts, many=True)
        return Response(postSerializer.data)

    elif request.method == "POST":
        # data = JSONParser().parse(request)
        # postSerializer = PostSerializer(data=data)
        postSerializer = PostSerializer(data=request.data)

        if postSerializer.is_valid():
            postSerializer.save()
            return Response(postSerializer.data, status=status.HTTP_201_CREATED)
        return Response(postSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def PostDetail(request, pk):

    try:
        post = Post.objects.get(pk=pk)

    except Post.DoesNotExist:
        return Response(
            {"message": "The post does not exist"}, status=status.HTTP_404_NOT_FOUND
        )

    if request.method == "GET":
        postSerializer = PostSerializer(post)
        return Response(postSerializer.data)

    elif request.method == "PUT":
        # data = JSONParser().parse(request)
        # serializer = PostSerializer(post, data=data)
        serializer = PostSerializer(post, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        post.delete()
        return Response({"message": "Post was deleted successfully!"})
