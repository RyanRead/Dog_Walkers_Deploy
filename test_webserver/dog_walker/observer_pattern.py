from .models import PointOfInterests


class Subject:
    observer_list = []

    def register(self, observer):
        for temp_observer in self.observer_list:
            if temp_observer.id == observer.id:
                return

        print('Adding Observer')
        self.observer_list.append(observer)

    def remove(self, observer):
        self.observer_list.remove(observer)

    def notify(self):
        for observer in self.observer_list:
            observer.update()

    def get_all_observers(self):
        return self.observer_list


class MapState(Subject):
    points_of_interest = []

    def get_poi(self):
        return self.points_of_interest

    def set_poi(self, points):
        self.points_of_interest = points


class Observer:
    id = ""

    def set_id(self, id):
        self.id = id


class MapView(Observer):

    # Refresh page
    def update(self):
        pass



