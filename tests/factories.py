"""
Test Factory to make fake objects for testing
"""
import factory
from factory.fuzzy import FuzzyChoice, FuzzyFloat
from service.models import Supplier

class SupplierFactory(factory.Factory):
    """Creates fake suppliers"""

    class Meta:
        """Meta class
        """
        model = Supplier

    id = factory.Sequence(lambda n: n)
    name = factory.Faker("company")
    phone = factory.Faker("phone_number")
    address = factory.Faker("address")
    available = FuzzyChoice(choices=[True, False])
    favorite = FuzzyChoice(choices=[True, False])
    product_list = FuzzyChoice(choices=[[1, 2, 3], [2, 3, 4], [3, 4, 5], [4, 5, 6]])
    rating = FuzzyFloat(0, 5, 2)
