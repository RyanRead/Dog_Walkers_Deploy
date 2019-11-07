from .models import *
from leaflet.admin import LeafletGeoAdmin
from django.contrib import admin


class PointOfInterestsAdmin(LeafletGeoAdmin):
    list_display = ('id', 'name', 'location')


class DogBreedsAdmin(admin.ModelAdmin):
    list_display = ('id', 'breed_name')


class DogsAdmin(admin.ModelAdmin):
    list_display = ('id', 'dog_name')


class WalkingRouteAdmin(admin.ModelAdmin):
    list_display = ('id', 'walking_route_name')


class WalkingClassAdmin(admin.ModelAdmin):
    list_display = ('id', 'class_name')


class JoinedClassAdmin(admin.ModelAdmin):
    # list_display = ('id'
    pass


class RecordedExerciseAdmin(admin.ModelAdmin):
    # list_display = ('id')
    pass


admin.site.register(PointOfInterests, PointOfInterestsAdmin)
admin.site.register(DogBreeds, DogBreedsAdmin)
admin.site.register(Dogs, DogsAdmin)
admin.site.register(WalkingRoute, WalkingRouteAdmin)
admin.site.register(WalkingClass, WalkingClassAdmin)
admin.site.register(JoinedClass, JoinedClassAdmin)
admin.site.register(RecordedExercise, RecordedExerciseAdmin)
admin.site.register(Profile)

