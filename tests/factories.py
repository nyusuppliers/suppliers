"""
Test Factory to make fake objects for testing
"""
import factory
from factory.fuzzy import FuzzyChoice, FuzzyFloat
from service.models import Supplier, Gender


class SupplierFactory(factory.Factory):
    """Creates fake suppliers"""

    class Meta:
        model = Supplier

    id = factory.Sequence(lambda n: n)
    name = factory.Faker("company")
    phone = factory.Faker("phone_number")
    address = factory.Faker("address")
    available = FuzzyChoice(choices=[True, False])
    product_list = FuzzyChoice(choices=[[1, 2, 3], [2, 3, 4], [3, 4, 5]])
    rating = FuzzyFloat(0, 5, 2)
