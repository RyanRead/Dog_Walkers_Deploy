from django.contrib import admin
from .models import LatLngPins, DogBreeds, Dogs
from leaflet.admin import LeafletGeoAdmin


class LatLngPinsAdmin(LeafletGeoAdmin):
    list_display = ('id', 'name', 'location')
    # pass


class DogBreedsAdmin(admin.ModelAdmin):
    list_display = ('id', 'breed_name')
    # pass


class DogsAdmin(admin.ModelAdmin):
    list_display = ('id', 'dog_name')
    # pass

admin.site.register(LatLngPins, LatLngPinsAdmin)
admin.site.register(DogBreeds, DogBreedsAdmin)
admin.site.register(Dogs, DogsAdmin)

