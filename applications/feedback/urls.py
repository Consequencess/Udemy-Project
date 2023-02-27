from django.urls import path, include
from rest_framework.routers import DefaultRouter

from applications.feedback import views

router = DefaultRouter()
router.register('comment', views.CommentViewSet, basename='comments')
router.register('like_comment', views.LikeDislikeCommentAPIView, basename='like_comment')
router.register('rating', views.RatingAPIView, basename='ratings')
router.register('wishlist', views.WishlistAPIView, basename='wishlists')

urlpatterns = [
    path('', include(router.urls))
]