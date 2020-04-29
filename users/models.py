from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.shortcuts import reverse
from main_object.functions import gen_slug
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='creator/default.jpg', upload_to='profile_pics')
    name = models.CharField("Name", max_length=150)
    dob = models.DateField(null=True, blank=True)
    # age = models.PositiveSmallIntegerField("Age", default=18)
    about = models.TextField("Description")
    #
    slug = models.SlugField(max_length=150, blank=True, unique=True)

    # def get_absolute_url(self):
    #     return reverse('user-detail', args=[str(self.pk)])

    def __str__(self):
        return f'{self.user.username} Profile'

    def get_absolute_url(self):
        return reverse('user_profile', args=[str(self.slug)])

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.user.username)
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
