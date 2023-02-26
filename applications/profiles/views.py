from django.shortcuts import render
from rest_framework import viewsets, permissions

from applications.profiles.models import Profile
from applications.profiles.serializers import ProfileSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
