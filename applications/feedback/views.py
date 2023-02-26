from rest_framework import mixins, viewsets
from rest_framework import permissions

from applications.feedback.mixins import LikeDislikeCommentMixin, ArchiveMixin, RatingMixin
from applications.feedback.models import Comment, LikeDislikeComment, Archive, Rating
from applications.feedback.permissions import IsCommentArchiveOwner
from applications.feedback.serializers import LikeDislikeCommentSerializer, CommentSerializer, ArchiveSerializer, \
    RatingSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsCommentArchiveOwner]

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


class ArchiveAPIView(mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                     mixins.ListModelMixin, ArchiveMixin, viewsets.GenericViewSet):
    queryset = Archive.objects.all()
    serializer_class = ArchiveSerializer
    permission_classes = [IsCommentArchiveOwner]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(owner=self.request.user)
        return queryset


