import random

from django.test import TestCase
from django.urls import reverse

from main.models import Bulletin


def bulletin_create(**kwargs):
    return Bulletin.objects.create(
        name=kwargs['name'],
        price=kwargs['price'],
        main_photo=kwargs['main_photo'],
        description=kwargs['description']
    )


class BulletinsListViewTests(TestCase):

    @staticmethod
    def create_test_bulletins(count):
        for _ in range(count):
            bulletin_create(
                name='test bulletin',
                price=115,
                main_photo='test photo',
                description='test description'
            )

    def get_bulletins_response(self, url=None):
        if url:
            return self.client.get(url)
        return self.client.get(reverse('main:bulletins'))

    def test_no_bulletins(self):
        response = self.client.get(reverse('main:bulletins'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 0)

    def test_one_bulletin(self):
        bulletin = bulletin_create(
            name='test bulletin',
            price=115,
            main_photo='test photo',
            description='test description'
        )
        response = self.get_bulletins_response()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)
        results = response.data['results'][0]
        for field, value in results.items():
            self.assertEqual(value, bulletin.__getattribute__(field))

    def test_many_bulletins(self):
        n_bulletins = random.randint(10, 40)
        self.create_test_bulletins(n_bulletins)
        response = self.get_bulletins_response()
        self.assertEqual(response.data['count'], n_bulletins)

    def test_paginated_bulletins(self):
        n_bulletins = random.randint(11, 19)
        self.create_test_bulletins(n_bulletins)
        response = self.get_bulletins_response()
        self.assertEqual(response.data['count'], n_bulletins)
        next_page = response.data['next']
        next_response = self.get_bulletins_response(next_page)

        self.assertEqual(
            len(next_response.data['results']),
            n_bulletins - 10
        )

    def test_price_sorting_bulletins(self):
        pass

    def test_data_sorting_bulletins(self):
        pass