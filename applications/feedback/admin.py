from django.contrib import admin

from applications.feedback.models import Comment, Rating, LikeDislikeComment, Wishlist

admin.site.register(Comment)
admin.site.register(Rating)
admin.site.register(LikeDislikeComment)
admin.site.register(Wishlist)