from django.db.models import Avg
from rest_framework import serializers
from applications.feedback.models import Rating, LikeDislikeComment, Comment, Wishlist


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(required=False)


    class Meta:
        model = Comment
        fields = '__all__'

    def to_representation(self, instance):
        res = super().to_representation(instance)
        res['course'] = instance.course.title
        return res


class LikeDislikeCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = LikeDislikeComment
        fields = ['like', 'comment']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        images = []
        for i in rep['images']:
            images.append(i['image'])
        rep['images'] = images
        # rep['images'] = instance.course.images
        rep['comment'] = instance.course.title
        if instance.like is True:
            rep['like'] = 'Liked'
        else:
            rep['like'] = 'Unliked'
        return rep


class RatingSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(min_value=1, max_value=5)
    course = serializers.CharField(required=False)

    class Meta:
        model = Rating
        fields = ['rating', 'course']


class WishlistSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(source='course.image')
    title = serializers.CharField(source='course.title')
    teacher = serializers.CharField(source='course.user.first_name')
    rating = serializers.SerializerMethodField()
    price = serializers.DecimalField(source='course.price', max_digits=6, decimal_places=2)
    id = serializers.IntegerField(source='course.id')

    class Meta:
        model = Wishlist
        fields = ['image', 'title', 'teacher', 'rating', 'price', 'id']

    def get_rating(self, obj):
        rating = obj.course.ratings.all().aggregate(Avg('rating'))['rating__avg']
        return round(rating, 1) if rating is not None else None

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        return rep


