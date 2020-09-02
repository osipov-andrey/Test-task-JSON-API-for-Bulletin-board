import random
from datetime import timedelta, datetime

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


def create_bulletins():
    n_bulletins = random.randint(10, 20)
    for number in range(n_bulletins):
        bulletin_create(
            name=number,
            price=number,
            main_photo=number,
            description=number
        )
    return n_bulletins


D1 = datetime.strptime('1/1/2008 1:30 PM', '%m/%d/%Y %I:%M %p')
D2 = datetime.strptime('1/1/2020 4:50 AM', '%m/%d/%Y %I:%M %p')


def random_date(start, end):
    """
    This function will return a random datetime between two datetime
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)


class BulletinsListViewTests(TestCase):
    """ Тестирование выдачи списка объявлений """
    @staticmethod
    def create_test_bulletins(count):
        """ Создаем сразу несколько объявлений в БД """
        for _ in range(count):
            bulletin_create(
                name='test bulletin',
                price=115,
                main_photo='test photo',
                description='test description'
            )

    def get_bulletins_response(self, url=None):
        """ Получаем объявления по API """
        if url:
            return self.client.get(url)
        return self.client.get(reverse('main:bulletins'))

    def test_no_bulletins(self):
        """ В БД нет объявлений """
        response = self.client.get(reverse('main:bulletins'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 0)

    def test_one_bulletin(self):
        """ В БД одно объявление """
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
        """ В БД несколько объявлений """
        n_bulletins = random.randint(10, 40)
        self.create_test_bulletins(n_bulletins)
        response = self.get_bulletins_response()
        self.assertEqual(response.data['count'], n_bulletins)

    def test_paginated_bulletins(self):
        """ Проверка пагинации """
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
        """ Тестирование сортировки объявлений по имени в разные направления """
        for number in range(10):
            bulletin_create(
                name=number,
                price=number,
                main_photo=number,
                description=number
            )
        response = self.client.get(reverse('main:bulletins') + '?sort=name')
        results = response.data['results']
        desc_response = self.client.get(reverse('main:bulletins') + '?sort=name&desc')
        desc_results = desc_response.data['results']

        self.assertEqual(list(reversed(results)), list(desc_results))

    def test_date_sorting_bulletins(self):
        """ Тестирование сортировки объявлений по дате в разные направления """
        for number in range(10):
            Bulletin.objects.create(
                name=number,
                price=number,
                main_photo=number,
                date=random_date(D1, D2),
                description=number
            )
        response = self.client.get(reverse('main:bulletins') + '?sort=date')
        results = response.data['results']
        desc_response = self.client.get(reverse('main:bulletins') + '?sort=date&desc')
        desc_results = desc_response.data['results']

        self.assertEqual(list(results), list(reversed(desc_results)))


class BulletinDetailViewTests(TestCase):

    def test_necessary_fields(self):
        """ В выдаче только обязательные поля объявления """
        n_bulletins = create_bulletins()
        pk = random.randint(10, n_bulletins)

        response = self.client.get(reverse('main:bulletin', kwargs={'pk': pk}))
        self.assertEqual(len(response.data), 3)
        self.assertIn('name', response.data)
        self.assertIn('price', response.data)
        self.assertIn('main_photo', response.data)

    def test_all_fields(self):
        """ В выдаче все поля объявления """
        n_bulletins = create_bulletins()
        pk = random.randint(10, n_bulletins)
        response = self.client.get(reverse('main:bulletin', kwargs={'pk': pk}) + '?fields')

        for field in Bulletin._meta.fields:
            self.assertIn(field.attname, response.data)


class BulletinCreateViewTests(TestCase):

    CREATE_PATTERN = {
        "additionalimages": [],
        "name": "test_name",
        "price": 1,
        "main_photo": "test_name",
        "description": "test_name",
    }

    def test_create_bulletin(self):
        """ Создание объявления """
        n_bulletins = create_bulletins()

        create_data = dict(**self.CREATE_PATTERN)
        create_data['additionalimages'] = [{"image": "test_path_to_image"}]

        response = self.client.post(
            reverse('main:create'),
            data=create_data,
            content_type='application/json'
        )
        self.assertEqual(response.data['id'], n_bulletins + 1)

    def test_create_bulletin_with_many_photos(self):
        """ Тест на создание объявления с числом картинок большим валидного """
        create_data = dict(**self.CREATE_PATTERN)
        create_data['additionalimages'] = [
            {"image": "test_path_to_image"} for _ in range(4)
        ]
        response = self.client.post(
            reverse('main:create'),
            data=create_data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('Too many images!', response.data['additionalimages'][0])
