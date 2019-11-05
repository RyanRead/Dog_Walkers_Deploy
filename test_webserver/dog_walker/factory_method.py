
class Product():
    message = ""

    def get_message(self):
        return self.message


class ConcreteProductErrorEmptyField(Product):
    message = "You Must fill in all fields"


class ConcreteProductErrorMustBeImage(Product):
    message = "The File you Uploaded must be an Image"


class ConcreteProductSuccessAddDog(Product):
    message = "You Successfully Added A Dog"


class ConcreteProductSuccessAddPOI(Product):
    message = "You Successfully Saved a Point of Interest"


class ConcreteProductSuccessSaveLeisureWalkingRoute(Product):
    message = "You Successfully Saved a Leisure Walking Route"


class ConcreteProductSuccessSaveTrainingWalkingRoute(Product):
    message = "You Successfully Saved a Training Walking Route"


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


class ConcreteErrorMessageCreator(Creator):
    def createProduct(self, type):
        if type == "empty_field":
            error_empty_field = ConcreteProductErrorEmptyField()
            return error_empty_field
        elif type == "not_image":
            error_not_image = ConcreteProductErrorMustBeImage()
            return error_not_image
