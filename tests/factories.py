'''
FACTORIES
'''
import factory
from factory.fuzzy import FuzzyChoice
from service.models.supplier_model import Supplier, Gender
from service.models.product_model import Product


class ProductFactory(factory.Factory):
    """ product factory """
    class Meta:
        """ product factory meta """
        model = Product

    product_id = factory.Sequence(lambda n: n)
    name = factory.Faker("name")
    price = factory.Faker("random_number")
    supplier_id = factory.Faker("random_number")

class SupplierFactory(factory.Factory):
    """ supplier factory """
    class Meta:
        """ supplier factory meta class """
        model = Supplier

    supplier_id = factory.Sequence(lambda n : n)
    name = factory.Faker("name")
    email = factory.Faker("email")
    phone = factory.Faker("phone_number")
    address = factory.Faker("address")
    available = FuzzyChoice(choices=[True, False])
    gender = FuzzyChoice(choices=[Gender.MALE, Gender.FEMALE, Gender.UNKNOWN])
