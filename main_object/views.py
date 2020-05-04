from django.shortcuts import render
# from rest_framework.views import APIView
from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework.response import Response

from django.db import models

from .models import MainObject
# from django.contrib.auth.models import User
from users.models import Profile


from .serialisers import MainObjectSerializer, MainObjectDetailSerializer,\
    ReviewCreateSerializer, CreateRankSerializer, ProfileListSerializer,\
    ProfileDetailSerializer
from .functions import get_client_ip
from .utils import MainObjectFilter


class MainObjectListView(generics.ListAPIView):
    """object list"""
    serializer_class = MainObjectSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MainObjectFilter
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        objects = MainObject.objects.filter(draft=False).annotate(
            # rank_user=models.Case(
            #     models.When(ranks__ip=get_client_ip(self.request), then=True),
            #     default=False,
            #     output_field=models.BooleanField()
            # ),
            rank_user=models.Count("ranks", filter=models.Q(ranks__ip=get_client_ip(self.request)))).annotate(
                middle_value=models.Sum(models.F('ranks__value'))/models.Count(models.F('ranks'))
            )
        return objects

        # serializer = MainObjectSerializer(objects, many=True)


# class MainObjectDetailView(APIView):
#     """object detail"""
#
#     def get(self, request, pk):
#         objects = MainObject.objects.get(id=pk, draft=False)
#         serializer = MainObjectDetailSerializer(objects)
#         return Response(serializer.data)


class MainObjectDetailView(generics.RetrieveAPIView):
    """ object detail view """
    queryset = MainObject.objects.filter(draft=False)
    serializer_class = MainObjectDetailSerializer


# class ReviewCreateView(APIView):
#     """add comment"""
#
#     def post(self, request):
#         review = ReviewCreateSerializer(data=request.data)
#         if review.is_valid():
#             review.save()
#         return Response(status=201)


class ReviewCreateView(generics.CreateAPIView):
    """ add comments to object"""
    serializer_class = ReviewCreateSerializer


# class AddValueRankView(APIView):
#     """
#     add rank to object
#     """
#     def post(self, request):
#         serializer = CreateRankSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(ip=get_client_ip(request))
#             return Response(status=201)
#         else:
#             return Response(status=400)


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

