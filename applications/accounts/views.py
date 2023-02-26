from datetime import datetime, timezone

from django.shortcuts import render
from rest_framework import views
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

# from datetime import datetime

from applications.accounts.serializers import (
    StudentRegisterSerializer, TeacherRegisterSerializer, ForgotPasswordSerializer, ForgotPasswordConfirmSerializer,
)
from applications.accounts.tasks import send_confirmation_email, send_confirmation_email_mentor

User = get_user_model()


class StudentRegisterAPIView(views.APIView):
    def post(self, request):
        serializer = StudentRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            send_confirmation_email(user.email, user.activation_code)
            return Response({"msg": "Вы успешно зарегистрировались, к вам почту отправили письмо с активацией вашего профиля"},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeacherRegisterAPIView(views.APIView):
    def post(self, request):
        serializer = TeacherRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            send_confirmation_email_mentor(user.email, user.activation_code)
            return Response({"msg": "Вы успешно зарегистрировались, к вам почту отправили письмо с активацией вашего профиля"},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivationAPIView(views.APIView):
    def get(self, request, activation_code, is_mentor=False):
        try:
            user = User.objects.get(activation_code=activation_code)
            user.is_active = True
            user.is_mentor = is_mentor
            user.activation_code = ""
            user.save()
            return Response(
                {"msg": "Successfully activated."},
                status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            return Response(
                {"msg": "Wrong email."},
                status=status.HTTP_400_BAD_REQUEST
            )


class TeacherActivationAPIView(ActivationAPIView):
    def get(self, request, activation_code):
        return super().get(request, activation_code, is_mentor=True)


class StudentActivationAPIView(ActivationAPIView):
    def get(self, request, activation_code):
        return super().get(request, activation_code, is_mentor=False)


class ForgotPasswordAPIView(views.APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.send_code()
        return Response({"msg": "Мы выслали ссылку для сброса пароля."})


class NewPasswordAPIView(views.APIView):

    def post(self, request, activation_code):
        user = User.objects.get(activation_code=activation_code)
        if (datetime.now(timezone.utc) - user.created_at).total_seconds() > 86400:
            return Response(
                {"msg": "Ссылка для сброса пароля недействительна."},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = ForgotPasswordConfirmSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.set_new_password()
        return Response(
            {"msg": "Пароль успешно обновлен."},
            status=status.HTTP_200_OK
        )
