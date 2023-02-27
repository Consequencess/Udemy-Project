from rest_framework import mixins, viewsets
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from applications.feedback.mixins import LikeDislikeCommentMixin, RatingMixin, WishlistMixin
from applications.feedback.models import Comment, LikeDislikeComment, Rating, Wishlist
from applications.feedback.permissions import IsCommentFavoriteOwner
from applications.feedback.serializers import LikeDislikeCommentSerializer, CommentSerializer, RatingSerializer,\
    WishlistSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsCommentFavoriteOwner]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LikeDislikeCommentAPIView(mixins.ListModelMixin,
                                LikeDislikeCommentMixin,
                                viewsets.GenericViewSet):
    queryset = LikeDislikeComment.objects.all()
    serializer_class = LikeDislikeCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(owner=self.request.user)
        return queryset


class RatingAPIView(mixins.ListModelMixin, mixins.DestroyModelMixin,
                    RatingMixin, viewsets.GenericViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(owner=self.request.user)
        return queryset


class WishlistAPIView(mixins.RetrieveModelMixin, mixins.ListModelMixin,
                      WishlistMixin, viewsets.GenericViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(owner=self.request.user)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset:
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({'message': 'Your wishlist is empty. Visit our homepage to find some great courses!',
                             'homepage': 'http://127.0.0.1:8000/api/v1/course/'})





