from time import sleep
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from django.contrib.auth import get_user_model

from applications.accounts.tasks import *

User = get_user_model()


class BaseUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6)

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name']

    def validate_password_confirm(self, value):
        password = self.initial_data.get('password')
        if password != value:
            raise serializers.ValidationError('Passwords do not match')

        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        code = user.activation_code
        send_confirmation_email.delay(user.email, code)
        return user


class StudentRegisterSerializer(BaseUserSerializer):
    pass


class TeacherRegisterSerializer(BaseUserSerializer):
    experience = serializers.ChoiceField(
        choices=[
            ('personally, privately', 'personally, privately'),
            ('personally, professionally', 'personally, professionally'),
            ('online', 'online'),
            ('other', 'other'),
        ],
        required=True
    )
    audience = serializers.ChoiceField(
        choices=[
            ('not at the moment', 'not at the moment'),
            ('I have a small audience', 'I have a small audience'),
            ('I have a sufficient audience', 'I have a sufficient audience'),
        ],
        required=True
    )

    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields + ['experience', 'audience']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        code = user.activation_code
        send_confirmation_email_mentor.delay(user.email, code)
        return user


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, email):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Такого пользователя не существует.")
        self.user = user
        return email

    def send_code(self):
        user = self.user
        user.create_activation_code()
        user.save()
        send_password_recovery.delay(user.email, user.activation_code)
        sleep(3)
        user.activation_code = ""


class ForgotPasswordConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=6, write_only=True, required=True)
    password_confirm = serializers.CharField(min_length=6, write_only=True, required=True)

    def validate_email(self, email):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Такого пользователя не существует.")
        self.user = user
        return email

    def validate(self, attrs):
        password = attrs.get("password")
        password_confirm = attrs.get("password_confirm")

        if password != password_confirm:
            raise serializers.ValidationError("Пароли не совпадают.")
        return attrs

    def set_new_password(self):
        user = self.user
        user.password = make_password(self.validated_data.get("password"))
        user.save()

