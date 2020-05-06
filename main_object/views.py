from django.shortcuts import render
# from rest_framework.views import APIView
from rest_framework import generics, permissions
# from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from django.db import models

from .models import MainObject
# from django.contrib.auth.models import User
from users.models import Profile
from .utils import MainObjectFilter


from .serialisers import MainObjectSerializer, MainObjectDetailSerializer,\
    ReviewCreateSerializer, CreateRankSerializer, ProfileListSerializer,\
    ProfileDetailSerializer, MainObjectCreateSerializer, MainObjectUpdateSerializer
from .functions import get_client_ip


class IsAuthorOrStaffOrReadOnly(permissions.BasePermission):
    """
    permission check is current user staff or object author
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.author or request.user.is_staff


class MainObjectListView(generics.ListAPIView):
    """object list"""

    serializer_class = MainObjectSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MainObjectFilter
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        objects = MainObject.objects.filter(draft=False).annotate(
            rank_user=models.Count(
                "ranks", filter=models.Q(
                    ranks__ip=get_client_ip(self.request)))).annotate(
            middle_value=models.Sum(models.F('ranks__value')) / models.Count(models.F('ranks')))
        return objects


class MainObjectDetailView(generics.RetrieveAPIView):
    """ object detail view """
    queryset = MainObject.objects.filter(draft=False)
    serializer_class = MainObjectDetailSerializer
    permission_classes = [IsAuthorOrStaffOrReadOnly]


class ReviewCreateView(generics.CreateAPIView):
    """add comment"""
    serializer_class = ReviewCreateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class MainObjectCreateView(generics.CreateAPIView):
    """ create object"""
    serializer_class = MainObjectCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class MainObjectUpdateView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MainObjectUpdateSerializer
    queryset = MainObject.objects.all()
    permission_classes = [IsAuthorOrStaffOrReadOnly]


class AddValueRankView(generics.CreateAPIView):
    serializer_class = CreateRankSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))


class ProfileListView(generics.ListAPIView):
    """list of users"""
    queryset = Profile.objects.all()
    serializer_class = ProfileListSerializer


class ProfileDetailView(generics.RetrieveAPIView):
    """list of users"""
    queryset = Profile.objects.all()
    serializer_class = ProfileDetailSerializer

