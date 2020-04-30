from rest_framework import serializers

from users.models import Profile
from django.contrib.auth.models import User

from .models import MainObject, Review, Rank


class AuthorSerializer(serializers.Serializer):
    """
    author profile info
    """
    class Meta:
        model = Profile
        fields = [
            "username", "image"
        ]


class FilterReviewListSerializer(serializers.ListSerializer):
    """
    comments filter (only parent)
    """
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):
    """
    recursive output children
    """
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class ProfileListSerializer(serializers.ModelSerializer):
    """users list"""
    user = serializers.SlugRelatedField(slug_field="username", read_only=True)
    class Meta:
        model = Profile
        fields = [
            "id",
            "user",
            "image",
        ]


class ProfileDetailSerializer(serializers.ModelSerializer):
    """user detail"""
    # user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = [
            "id",
            "image",
            "name",
            "about",
            "dob",
        ]


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileDetailSerializer(read_only=True)
    class Meta:
        model = User
        fields = [
            'username',
            'profile',
            'last_login',
            'is_staff',
            'is_active',
            'date_joined'
        ]


class MainObjectSerializer(serializers.ModelSerializer):
    """
    objects list
    """

    rank_user = serializers.BooleanField()
    middle_value = serializers.IntegerField()
    class Meta:
        model = MainObject
        fields = [
            "id",
            "name",
            "about",
            "description",
            "image",
            "date_published",
            "category",
            "tag",
            "author",
            "rank_user",
            "middle_value"
        ]


class ReviewSerializer(serializers.ModelSerializer):
    """
    comment list
    """
    children = RecursiveSerializer(many=True)
    author = UserSerializer(read_only=True)

    class Meta:
        list_serializer_class = FilterReviewListSerializer
        model = Review

        fields = [
            "author",
            "text",
            "children",
            "date_published",
        ]


class ReviewCreateSerializer(serializers.ModelSerializer):
    """
    comments create
    """

    class Meta:
        model = Review
        fields = "__all__"


class MainObjectDetailSerializer(serializers.ModelSerializer):
    """
    object detail
    """
    category = serializers.SlugRelatedField(slug_field="slug", read_only=True)
    tag = serializers.SlugRelatedField(slug_field="slug", read_only=True, many=True)
    author = UserSerializer(read_only=True)
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = MainObject
        exclude = ("draft",)


class CreateRankSerializer(serializers.ModelSerializer):
    """Add Rank"""
    class Meta:
        model = Rank
        fields = ("value", "main_object")

    def create(self, validated_data):
        rank = Rank.objects.update_or_create(
            ip=validated_data.get("ip", None),
            main_object=validated_data.get("main_object", None),
            defaults={"value": validated_data.get("value")}
        )
        return rank
