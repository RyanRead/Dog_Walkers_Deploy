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
    dog_image = models.CharField(default='default.jpg', max_length=100)

    def __str__(self):
        return self.dog_name

    class Meta:
        verbose_name = 'Dog'
        verbose_name_plural = 'Dogs'


class WalkingRoute(models.Model):
    # TODO DO THIS
    ROUTE_TYPES = [
        ('Leisure', 'Leisure'),
        ('Training', 'Training')
    ]
    walking_route_name = models.CharField(max_length=25)

    walking_route_start = models.ForeignKey(
        PointOfInterests, related_name='StartPoint', null=False, on_delete=True)
    walking_route_middle_1 = models.ForeignKey(
        PointOfInterests, related_name='Stop1', null=True, blank=True, on_delete=True)
    walking_route_middle_2 = models.ForeignKey(
        PointOfInterests, related_name='Stop2', null=True, blank=True, on_delete=True)
    walking_route_middle_3 = models.ForeignKey(
        PointOfInterests, related_name='Stop3', null=True, blank=True, on_delete=True)
    walking_route_end = models.ForeignKey(
        PointOfInterests, related_name='EndPoint', null=False, on_delete=True)

    walking_route_duration = models.PositiveSmallIntegerField()
    walking_route_type = models.CharField(max_length=10,
                                          choices=ROUTE_TYPES,
                                          default='Leisure')
    user_id = models.ForeignKey(User, on_delete=True)

    def __str__(self):
        return self.walking_route_name

    class Meta:
        verbose_name = 'Walking Route'
        verbose_name_plural = 'Walking Routes'


class WalkingClass(models.Model):
    class_name = models.CharField(max_length=20)
    class_instructor = models.ForeignKey(User, on_delete=False)
    walking_route_id = models.ForeignKey(WalkingRoute, on_delete=False)
    class_date = models.DateField()
    class_time = models.TimeField()
    class_participants = models.PositiveSmallIntegerField()
    class_max_participants = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.class_name

    class Meta:
        verbose_name = 'Walking Class'
        verbose_name_plural = 'Walking Classes'


class JoinedClass(models.Model):
    user_id = models.ForeignKey(User, on_delete=False)
    class_id = models.ForeignKey(WalkingClass, on_delete=False)

    class Meta:
        verbose_name = 'Joined Classes'
        verbose_name_plural = 'Joined Classes'


class RecordedExercise(models.Model):
    dog_id = models.ForeignKey(Dogs, on_delete='false')
    exercise_date = models.DateField()
    exercise_duration = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = 'Recorded Exercise'
        verbose_name_plural = 'Recorded Exercise'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_trainer = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} Profile'