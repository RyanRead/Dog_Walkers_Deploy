# from django.db import models
from django.contrib.gis.db import models
from django.contrib.auth.models import User


class PointOfInterests(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    creator = models.ForeignKey(User, on_delete=False)
    location = models.PointField(srid=4326)
    category = models.CharField(max_length=20)
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Point of Interest'
        verbose_name_plural = 'Points of Interest'


class DogBreeds(models.Model):
    breed_name = models.CharField(max_length=100)
    breed_average_weight = models.PositiveSmallIntegerField()
    breed_average_lifespan = models.PositiveSmallIntegerField()
    breed_daily_exercise_needs = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.breed_name

    class Meta:
        verbose_name = 'Dog Breed'
        verbose_name_plural = 'Dog Breeds'


class Dogs(models.Model):
    user_id = models.ForeignKey(User, on_delete=False)
    dog_name = models.CharField(max_length=100)
    dog_breed_id = models.ForeignKey(DogBreeds, on_delete=False)
    dog_age = models.PositiveSmallIntegerField()
    dog_weight = models.PositiveSmallIntegerField()
    dog_image = models.CharField(max_length=100)

    def __str__(self):
        return self.dog_name

    class Meta:
        verbose_name = 'Dog'
        verbose_name_plural = 'Dogs'