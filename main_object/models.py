# from datetime import date
# from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User

from .functions import ObjectAutoSlug
# from likes.models import Like
# Create your models here.


class Category(ObjectAutoSlug, models.Model):
    """Main Object Categories"""
    name = models.CharField("Category", max_length=150)
    description = models.TextField("Description", blank=True)
    slug = models.SlugField(max_length=150, blank=True, unique=True)

    def get_absolute_url(self):
        return reverse('category-detail', args=[str(self.slug)])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Tag(ObjectAutoSlug, models.Model):
    """ Tags for Main Object"""
    name = models.CharField("Name", max_length=150)
    description = models.TextField("Description")
    slug = models.SlugField(max_length=150, unique=True, blank=True)

    def get_absolute_url(self):
        return reverse('tag-detail', args=[str(self.slug)])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"


class MainObject(ObjectAutoSlug, models.Model):
    """Main Object"""
    name = models.CharField("Name", max_length=200)
    about = models.CharField("About", max_length=200, default='')
    description = models.TextField("Description")
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField("Main Image", blank=True, upload_to='MainObject/', default='MainObject/default.jpg')
    date_create = models.PositiveSmallIntegerField("Date Create", default=2020)
    date_published = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, blank=True, on_delete=models.SET_NULL, null=True)
    country = models.CharField("Country", max_length=50)
    tag = models.ManyToManyField(Tag, verbose_name="tag1", blank=True, related_name='tags')

    slug = models.SlugField(max_length=200, unique=True, blank=True)
    draft = models.BooleanField("Draft", default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # """add likes model"""
    # likes = GenericRelation(Like)

    def __str__(self):
        return self.name

    # @property
    # def total_likes(self):
    #     return self.likes.count()

    # noinspection SpellCheckingInspection
    def get_review(self):
        return self.review_set.filter(parent__isnull=True)

    def get_absolute_url(self):
        return reverse('object-detail', args=[str(self.slug)])

    def get_update_url(self):
        return reverse('object-update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('object-delete_url', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['-date_published']
        verbose_name = "Main Object"
        verbose_name_plural = "Main Objects"


class AdditionalObjects(models.Model):
    """Additional Objects in Main Object"""
    title = models.CharField("Title", max_length=100)
    description = models.TextField("Description")
    image = models.ImageField("More image for Main Object", blank=True, upload_to='object_in_objects/')
    main_object = models.ForeignKey(MainObject, verbose_name="MainObject", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Additional Object"
        verbose_name_plural = "Additional Objects"


class RankValue(models.Model):
    """Rank Value"""
    value = models.SmallIntegerField("Value", default=0)

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = "Value of Object Rank"
        verbose_name_plural = "Values of Object Rank"


class Rank(models.Model):
    """Rank"""
    ip = models.CharField("IP", max_length=15)
    value = models.ForeignKey(RankValue, on_delete=models.CASCADE, verbose_name="value")
    main_object = models.ForeignKey(MainObject, on_delete=models.CASCADE, verbose_name="main object")

    def __str__(self):
        return "{} - {}".format(self.value, self.main_object)

    class Meta:
        verbose_name = "Rank"
        verbose_name_plural = "Ranks"


class Review(models.Model):
    """Comments"""
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField("Message", max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name="Parent", on_delete=models.SET_NULL, blank=True, null=True
    )
    main_object = models.ForeignKey(MainObject, verbose_name="main object", on_delete=models.CASCADE)
    date_published = models.DateTimeField(auto_now_add=True)
    # likes = GenericRelation(Like)

    def __str__(self):
        return "{} - {} - {}".format(self.id, self.main_object, self.author)

    # @property
    # def total_likes(self):
    #     return self.likes.count()

    class Meta:
        ordering = ['-date_published']
        verbose_name = "Review"
        verbose_name_plural = "Reviews"


# class UnRegComment(models.Model):
#     """Comments from unregistered users"""
#     email = models.EmailField()
#     name = models.CharField("Name", max_length=100)
#     text = models.TextField("Message", max_length=5000)
#     parent = models.ForeignKey(
#         'self', verbose_name="Parent", on_delete=models.SET_NULL, blank=True, null=True
#     )
#     main_object = models.ForeignKey(MainObject, verbose_name="main object", on_delete=models.CASCADE)
#
#     def __str__(self):
#         return "{} - {}".format(self.name, self.main_object)
#
#     class Meta:
#
#         verbose_name = "Comment"
#         verbose_name_plural = "Comments"
