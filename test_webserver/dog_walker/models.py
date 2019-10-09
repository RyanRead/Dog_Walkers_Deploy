# from django.db import models
from django.contrib.gis.db import models
from django.contrib.auth.models import User


class LatLngPins(models.Model):
    name = models.CharField(max_length=100)
    info = models.TextField()
    creator = models.ForeignKey(User, on_delete=False)
    location = models.PointField(srid=4326)

    def __str__(self):
        return self.name


class DogBreeds(models.Model):
    breed_name = models.CharField(max_length=100)
    breed_average_weight = models.PositiveSmallIntegerField()
    breed_average_lifespan = models.PositiveSmallIntegerField()
    breed_daily_exercise_needs = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.breed_name

class Dogs(models.Model):
    user_id = models.ForeignKey(User, on_delete=False)
    dog_name = models.CharField(max_length=100)
    dog_breed_id = models.ForeignKey(DogBreeds, on_delete=False)
    dog_age = models.PositiveSmallIntegerField()
    dog_weight = models.PositiveSmallIntegerField()
    dog_image = models.CharField(max_length=100)

    def __str__(self):
        return self.dog_name + 'henryisgay'