from rest_framework import serializers
from applications.course.models import Course
from applications.orders.tasks import send_confirm_link
from applications.orders.models import Order


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Order
        exclude = ['confirm_code', 'order_confirm']

    def create(self, validated_data):
        order = Order.objects.create(**validated_data)
        order.create_confirm_code()
        order.save()
        send_confirm_link.delay(order.user.email, order.confirm_code)
        return order

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        course = Course.objects.get(id=rep['course']).title
        rep['order_confirm'] = instance.order_confirm
        rep['course'] = course
        return rep
