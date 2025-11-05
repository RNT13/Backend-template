import factory
from faker import Faker

from products.models import Product

fake = Faker()


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.LazyAttribute(lambda _: fake.word())
    description = factory.LazyAttribute(lambda _: fake.text())
    price = factory.LazyAttribute(lambda _: fake.pydecimal(2, 2, True))
    stock = factory.LazyAttribute(lambda _: fake.random_int(1, 100))
