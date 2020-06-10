from django.test import TestCase
from api.models import Auto
import random
from rest_framework.test import APIClient


# Что протестировано
# GET api/auto
# POST api/auto
# DELETE api/auto
# GET api/auto/slug
# GET api/statistics

class ViewaTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Создание тестового набора данных из 20 записей в БД
        create_random_objects_in_base(20)

    def test_view_main_page(self):
        # Проверяем все ли объекты создались в БД
        self.assertEqual(Auto.objects.count(), 20)  # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

        # Тестируем корректность кода ответа сервера при разных случаях
        client = APIClient()
        response = client.get('/api/')

        # GET-запрос к главной странице
        self.assertEqual(response.status_code, 200)

        # Delete-запрос на удаление НЕсуществующего авто
        response = client.delete('/api/', {'vin_code': '123456789'}, format='json')
        self.assertEqual(response.status_code, 404)

        # Delete-запрос на удаление существующего авто
        new_auto = Auto(car_number='test', vin_code='vin_code_test',
                        color='color', mark='mark', year_of_issue=2020
                        )
        new_auto.save()

        response = client.delete('/api/', {'vin_code': 'vin_code_test'}, format='json')
        self.assertEqual(response.status_code, 204)

        # Тест POST-запроса добавления авто с корректной информацией
        response = client.post('/api/',
                               {
                                   "auto":
                                       {
                                           "car_number": "test_123",
                                           "vin_code": "123456789",
                                           "color": "color_test",
                                           "mark": "mark_test",
                                           "year_of_issue": 2020
                                       }
                               },
                               format='json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, {"message": "auto created successfully"})

        # Тест POST-запроса БЕЗ заполнения обязательного поля VIN_CODE
        response = client.post('/api/',
                               {
                                   "auto":
                                       {
                                           "car_number": "test_123",
                                           "color": "color_test",
                                           "mark": "mark_test",
                                           "year_of_issue": 2020
                                       }
                               },
                               format='json')

        self.assertEqual(response.status_code, 400)

        # Тест POST-запроса с заполнением ТОЛЬКО обязательного поля VIN_CODE
        response = client.post('/api/',
                               {
                                   "auto":
                                       {
                                           "vin_code": "00000000test",
                                       }
                               },
                               format='json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, {"message": "auto created successfully"})

        # Тест POST-запроса с НЕуникальным значением поля  VIN_CODE
        response = client.post('/api/',
                               {
                                   "auto":
                                       {
                                           "vin_code": "00000000test",
                                       }
                               },
                               format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'message': 'auto with vin code 00000000test exists'})

    def test_view_main_page_sort_by(self):
        # Тест работы сортировки
        client = APIClient()

        # GET-запрос к главной странице с некорректными параметрами сотрировки
        response = client.get('/api/?order_by=test_param')
        self.assertEqual(response.status_code, 200)

        response = client.get('/api/?order_____byyyyyyyy=test_param')
        self.assertEqual(response.status_code, 200)

        # Добавление авто с самым ранным годом производства
        new_auto = Auto(car_number='test', vin_code='vin_code_test',
                        color='color', mark='mark', year_of_issue=2010
                        )
        new_auto.save()

        # Добавление авто с самым поздним годом производства
        new_auto = Auto(car_number='test', vin_code='vin_code_test2',
                        color='color', mark='mark', year_of_issue=1800
                        )
        new_auto.save()

        # Добавление авто со средним значением годп производства
        new_auto = Auto(car_number='test', vin_code='vin_code_test4',
                        color='color', mark='mark', year_of_issue=2020
                        )
        new_auto.save()

        response = client.get('/api/?order_by=year_of_issue')
        data = response.data.get('auto')
        data_in_list = list(data)
        first = data_in_list[0]

        self.assertEqual(first['year_of_issue'], 1800)

    def test_get_auto_by_slug(self):
        # GET api/auto/slug

        new_auto = Auto(car_number='test', vin_code='test_slug',
                        color='color', mark='mark', year_of_issue=2020
                        )
        new_auto.save()

        client = APIClient()
        response = client.get('/api/test_slug/')
        self.assertEqual(response.status_code, 200)

        response = client.get('/api/broken_slug/')
        self.assertEqual(response.status_code, 404)

    def test_statistics_view(self):
        client = APIClient()
        response = client.get('/api/statistics/')
        self.assertEqual(response.status_code, 200)

        data = response.data
        self.assertEqual(data.get('count_auto'), 20)
        self.assertEqual(data.get('auto_without_numbers'), 0)


def create_random_objects_in_base(count_of_obj):
    population_chars = 'ABCDEKMHOPCTYX'

    for i in range(count_of_obj):
        car_number = str(''.join(random.sample(population_chars, 2))
                         + str(random.randint(100, 999))
                         + ''.join(random.sample(population_chars, 1))
                         )

        vin_code = str(''.join(random.sample(population_chars, 3))
                       + str(random.randint(100000000, 999999999))
                       + ''.join(random.sample(population_chars, 2))
                       )

        population_colors = ['красный', 'оранжевый', 'желтый',
                             'зеленый', 'голубой', 'синий', 'фиолетовый']

        color = random.sample(population_colors, 1)

        population_marks = ['Toyota', 'Lada', 'Volkswagen ', 'Mersedes-benz',
                            'Audi', 'Peugeot', 'Renault', 'Nissan', 'Mitsubishi',
                            'Hyundai', 'Ford', 'Tesla', 'Honda']

        mark = random.sample(population_marks, 1)

        year_of_issue = random.randint(1980, 2020)

        new_auto = Auto(car_number=car_number, vin_code=vin_code,
                        color=color, mark=mark, year_of_issue=year_of_issue
                        )
        new_auto.save()
