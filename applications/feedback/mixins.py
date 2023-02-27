from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from applications.feedback.models import Rating, LikeDislikeComment, Wishlist
from applications.feedback.serializers import RatingSerializer


class LikeDislikeCommentMixin:
    @action(detail=True, methods=['POST'])
    def post(self, request, pk, *args, **kwargs):
        obj, _ = LikeDislikeComment.objects.get_or_create(comment_id=pk, owner=request.user)
        obj.like = not obj.like
        obj.save()
        status_ = 'Liked'
        if not obj.like:
            status_ = 'Unliked'
        return Response({'msg': status_})


class RatingMixin:
    @action(detail=True, methods=['POST'])
    def post(self, request, pk, *args, **kwargs):
        serializer = RatingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj, _ = Rating.objects.get_or_create(course_id=pk, owner=request.user)
        obj.rating = request.data['rating']
        obj.save()
        return Response(request.data, status=status.HTTP_201_CREATED)


class WishlistMixin:

    @action(detail=True, methods=['POST'])
    def post(self, request, pk, *args, **kwargs):
        obj, _ = Wishlist.objects.get_or_create(course_id=pk, owner=request.user)
        obj.save()
        status_ = 'Added to wishlist'
        return Response({'msg': status_})

    @action(detail=True, methods=['DELETE'])
    def delete(self, request, pk, *args, **kwargs):
        try:
            obj = Wishlist.objects.get(course_id=pk, owner=request.user)
            obj.delete()
            status_ = 'Removed from wishlist'
        except Wishlist.DoesNotExist:
            status_ = 'Not found in wishlist'
        return Response({'msg': status_})