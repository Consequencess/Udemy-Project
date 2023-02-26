from django.shortcuts import render
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import views
from rest_framework import viewsets
from applications.orders.models import Order
from applications.orders.serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # def get_queryset(self):
    #     user = self.request.user
    #     queryset = super().get_queryset()
    #     res = queryset.filter(user=user)
    #     return res
    def get_queryset(self):
        queryset = Order.objects.all()
        user = self.request.user
        if user.is_authenticated:
            res = queryset.filter(user=user)
        else:
            res = queryset.none()
        return res


class OrderConfirm(views.APIView):
    @staticmethod
    def get(request, confirm_code):
        try:
            order = Order.objects.get(confirm_code=confirm_code)
            order.order_confirm = True
            order.confirm_code = ''
            course = order.course
            course.save()
            order.save()
            return Response({'msg': 'заказ подтвержден'}, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({'msg': 'неправильный код подверждение заказа'}, status=status.HTTP_400_BAD_REQUEST)


