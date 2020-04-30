from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response

from django.db import models

from .models import MainObject
# from django.contrib.auth.models import User
from users.models import Profile


from .serialisers import MainObjectSerializer, MainObjectDetailSerializer,\
    ReviewCreateSerializer, CreateRankSerializer, ProfileListSerializer,\
    ProfileDetailSerializer
from .functions import get_client_ip


class MainObjectListView(APIView):
    """object list"""

    def get(self, request):
        objects = MainObject.objects.filter(draft=False).annotate(
            # rank_user=models.Case(
            #     models.When(ranks__ip=get_client_ip(request), then=True),
            #     default=False,
            #     output_field=models.BooleanField()
            # ),
            rank_user=models.Count("ranks", filter=models.Q(ranks__ip=get_client_ip(request)))).annotate(
                middle_value=models.Sum(models.F('ranks__value'))/models.Count(models.F('ranks'))
            )

        serializer = MainObjectSerializer(objects, many=True)
        return Response(serializer.data)


class MainObjectDetailView(APIView):
    """object detail"""

    def get(self, request, pk):
        objects = MainObject.objects.get(id=pk, draft=False)
        serializer = MainObjectDetailSerializer(objects)
        return Response(serializer.data)


class ReviewCreateView(APIView):
    """add comment"""

    def post(self, request):
        review = ReviewCreateSerializer(data=request.data)
        if review.is_valid():
            review.save()
        return Response(status=201)


class AddValueRankView(APIView):
    """
    add rank to object
    """
    def post(self, request):
        serializer = CreateRankSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(ip=get_client_ip(request))
            return Response(status=201)
        else:
            return Response(status=400)


class ProfileListView(generics.ListAPIView):
    """list of users"""
    queryset = Profile.objects.all()
    serializer_class = ProfileListSerializer


class ProfileDetailView(generics.RetrieveAPIView):
    """list of users"""
    queryset = Profile.objects.all()
    serializer_class = ProfileDetailSerializer

