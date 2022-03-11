from django.test import TestCase
from .recommender import Recommender
from .models import Product, Category


class RecommendationEngineTestCase(TestCase):
    def setUp(self):
        food = Category.objects.create(name='Food')
        potato = Product(name='Potato', price=1)
        potato.category = food
        potato.save()
        banana = Product(name='Banana', price=1)
        banana.category = food
        banana.save()
        apple = Product(
            name='Golden Apple', price=1)
        apple.category = food
        apple.save()
        tomato = Product(name='Tomato', price=2)
        tomato.category = food
        tomato.save()

    def test_recommender(self):
        potato = Product.objects.get(name='Potato')
        banana = Product.objects.get(name='Banana')
        apple = Product.objects.get(name='Golden Apple')
        tomato = Product.objects.get(name='Tomato')
        rec = Recommender()

        rec.products_bought([potato, banana])
        rec.products_bought([potato, apple])
        rec.products_bought([potato, banana, tomato])
        rec.products_bought([apple, banana])
        rec.products_bought([tomato, apple])
        rec.products_bought([tomato, banana])

        self.assertEqual(len(rec.suggest_products_for([potato])), 3)
        self.assertEqual(len(rec.suggest_products_for([potato, banana])), 2)
        self.assertQuerysetEqual(rec.suggest_products_for([tomato]), [
                                 banana, apple, potato])
