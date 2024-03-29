from rest_framework import permissions, generics
from Pynet.base.classes import CreateUpdateDestroy, CreateRetrieveUpdateDestroy
from Pynet.base.permissions import IsAuthor
from .models import Post, Comment
from .serializers import (PostSerializer, ListPostSerializer, CreateCommentSerializer)


class PostListView(generics.ListAPIView):
    """ posts list on a wall
    """
    serializer_class = ListPostSerializer

    def get_queryset(self):
        return Post.objects.filter(
            user_id=self.kwargs.get('pk')).select_related('user').prefetch_related('comments')


class PostView(CreateRetrieveUpdateDestroy):
    """ CRUD of post
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Post.objects.all().select_related('user').prefetch_related('comments')
    serializer_class = PostSerializer
    permission_classes_by_action = {'get': [permissions.AllowAny],
                                    'update': [IsAuthor],
                                    'destroy': [IsAuthor]}

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentsView(CreateUpdateDestroy):
    """ CRUD comments for post
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CreateCommentSerializer
    permission_classes_by_action = {'update': [IsAuthor],
                                    'destroy': [IsAuthor]}

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()