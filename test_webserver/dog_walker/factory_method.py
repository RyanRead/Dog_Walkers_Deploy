
class Product():
    message = ""

    def get_message(self):
        return self.message

'''
ERRORS
'''

class ConcreteProductErrorEmptyField(Product):
    message = "You Must fill in all fields"


class ConcreteProductErrorMustBeImage(Product):
    message = "The File you Uploaded must be an Image"


class ConcreteProductErrorFullClass(Product):
    message = "Cannot Join Class as it is Full"


class ConcreteProductErrorPoi(Product):
    message = "Select a Marker on the Map"

'''
SUCCESS
'''

class ConcreteProductSuccessAddDog(Product):
    message = "You Successfully Added A Dog"


class ConcreteProductSuccessAddPOI(Product):
    message = "You Successfully Saved a Point of Interest"


class ConcreteProductSuccessSaveLeisureWalkingRoute(Product):
    message = "You Successfully Saved a Leisure Walking Route"


class ConcreteProductSuccessSaveTrainingWalkingRoute(Product):
    message = "You Successfully Saved a Training Walking Route"


class ConcreteProductSuccessSaveTrainingRecordExercise(Product):
    message = "You Successfully Recorded your Walk"


class ConcreteProductSuccessSaveWalkingClass(Product):
    message = "You Successfully Saved a New Walking Class"


class ConcreteProductSuccessJoinClass(Product):
    message = "You Successfully Joined Walking Class"


class Creator:
    def createProduct(self):
        pass


class ConcreteSuccessMessageCreator(Creator):
    def createProduct(self, type):
        if type == "add_dog":
            success_add_dog = ConcreteProductSuccessAddDog()
            return success_add_dog
        elif type == "add_poi":
            success_add_poi = ConcreteProductSuccessAddPOI()
            return success_add_poi
        elif type == "save_leisure_route":
            success_save_leisure_route = ConcreteProductSuccessSaveLeisureWalkingRoute()
            return success_save_leisure_route
        elif type == "save_training_route":
            success_save_training_route = ConcreteProductSuccessSaveTrainingWalkingRoute()
            return success_save_training_route
        elif type == "save_exercise":
            success_record_exercise = ConcreteProductSuccessSaveTrainingRecordExercise()
            return success_record_exercise
        elif type == "save_walking_class":
            success_walking_class = ConcreteProductSuccessSaveWalkingClass()
            return success_walking_class
        elif type == "join_walking_class":
            success_saving_class = ConcreteProductSuccessJoinClass()
            return success_saving_class


class ConcreteErrorMessageCreator(Creator):
    def createProduct(self, type):
        if type == "empty_field":
            error_empty_field = ConcreteProductErrorEmptyField()
            return error_empty_field
        elif type == "not_image":
            error_not_image = ConcreteProductErrorMustBeImage()
            return error_not_image
        elif type == "full_class":
            error_full_class = ConcreteProductErrorFullClass()
            return error_full_class
        elif type == "add_poi":
            error_poi = ConcreteProductErrorPoi()
            return error_poi
