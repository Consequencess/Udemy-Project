from rest_framework import serializers

from applications.feedback.models import Rating, LikeDislikeComment, Comment, Archive


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


class ArchiveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Archive
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['owner'] = instance.owner.email
        rep['course'] = instance.course.title
        return rep
