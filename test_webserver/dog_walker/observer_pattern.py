from django.core.mail import send_mail
from django.conf import settings


class Subject:
    observer_list = []

    def register(self, observer):
        pass

    def remove(self, observer):
        pass

    def notify(self):
        pass


class ConcreteSubject(Subject):
    walking_classes = []

    def register(self, observer):
        # for observer in self.observer_list:
        #     if observer.email == observer.email:
        #         return
        # print("Adding Observer " + observer.email)
        self.observer_list.append(observer)

    def remove(self, observer):
        self.observer_list.remove(observer)

    def notify(self):
        for observer in self.observer_list:
            observer.update(self.walking_classes[-1])

    # TODO Delete this
    def print_observers(self):
        print("The observers are:")
        for observer in self.observer_list:
            print(observer.email)


class Observer:
    def update(self, walking_class):
        pass


class ConcreteObserver(Observer):
    name = ''  # make private
    email = ''  # make private

    def __init__(self, name, email):
        """Initialize object state"""
        self.name = name
        self.email = email

    def set_name(self, name):
        self.name = name

    def set_email(self, email):
        self.email = email

    def get_name(self):
        return self.name

    def get_email(self):
        return self.email

    def update(self, walking_class):
        print("Sending Email to " + self.get_name() + " at " + self.get_email())
        # subject = 'This is an automated email. Please do not respond'
        # message = 'The walking class ' + walking_class + ' has been added! \n Log In to see more details!'
        # email_from = settings.EMAIL_HOST_USER
        # recipient_list = [self.get_email()]
        # send_mail(subject, message, email_from, recipient_list)
