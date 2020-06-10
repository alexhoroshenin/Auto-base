from rest_framework.response import Response
from .models import Auto
from django.db.models import Count
from .serializers import AutoSerializer
from rest_framework.views import APIView
from django.db import connection


class AutoListView(APIView):
    """Класс формирует отображение информациеи в JSON формате и/или в HTML для GET-запросов"""

    def get(self, request):
        """Обработка GET запроса с возможностью сортировки. Формировние ответа сервера"""

        ordering_param = request.query_params.get('order_by')

        # проверка наличия в запросе параметра для сортировки.
        # если параметр отсутствует и/или его значение не соответствует объекту, то сортировка не будет произведена
        if ordering_param and hasattr(Auto, ordering_param):
            all_auto = Auto.objects.all().order_by(ordering_param)
        else:
            all_auto = Auto.objects.all()

        serializer = AutoSerializer(all_auto, many=True)

        return Response({"auto": serializer.data},
                        status=200)

    def post(self, request):
        """Обработка POST-запроса с проверкой на наличие объекта в БД по уникальному полю vin_code.
        Если объект с таким vin_code уже есть, то сервер отправит сообщение об ошибке."""

        auto = request.data.get('auto')
        serializer = AutoSerializer(data=auto)

        if serializer.is_valid(raise_exception=True):
            vin_code = serializer.validated_data.get('vin_code')

        if serializer.auto_exist(vin_code):
            return Response({"message": "auto with vin code {} exists".format(vin_code)},
                            status=400)

        serializer.save()
        return Response({"message": "auto created successfully"},
                        status=201)

    def delete(self, request):
        """Обработа DELETE-запросов. Удаление производится по параметру vin_code.
        Если объект со занчегием этого параметра не существует, то сервер отправит сообщение об ошибке."""

        vin_code = request.data.get('vin_code')

        try:
            auto = Auto.objects.get(vin_code=vin_code)
        except:
            return Response({"message": "Auto with vin_code `{}` not exist.".format(vin_code)},
                            status=404)

        auto.delete()

        return Response({"message": "Auto with vin_code `{}` has been deleted.".format(vin_code)},
                        status=204)


class AutoDetailView(APIView):
    """Класс формирует отображение информациеи в JSON и HTML форматах для GET-запросов
    с указанным VIN_СODE  http://127.0.0.1:8000/api/auto/YOUR_VIN_СODE"""

    def get(self, request, slug):

        try:
            auto = Auto.objects.get(vin_code=slug)
        except:
            return Response({"message": 'Object with vin_code {} not exist'.format(slug)},
                            status=404)

        serializer = AutoSerializer(auto)

        return Response({"auto": serializer.data},
                        status=200)


class StatisticsView(APIView):
    """Класс формирует отображение статистики в JSON и HTML форматах для GET-запросов"""

    def get(self, request):

        all_auto = Auto.objects.all()  # все объекты БД
        count_auto = all_auto.count()  # количество объектов в БД

        if count_auto == 0:
            return Response({"message": "No information in the database"}, status=204)

        first_created_object = all_auto.order_by('creating_date').first()
        first_created_object_data = first_created_object.creating_date

        last_created_object = all_auto.order_by('creating_date').last()
        last_created_object_data = last_created_object.creating_date

        oldest_car, newest_car = self.get_oldest_and_newest_cars()

        auto_without_numbers = all_auto.filter(car_number=None).count()

        thin_mark, large_mark = self.get_large_and_thim_marks()

        response = {
            "count_auto": count_auto,
            "first_created_object_data": first_created_object_data,
            "last_created_object_data": last_created_object_data,
            "oldest_car": oldest_car,
            "newest_car": newest_car,
            "auto_without_numbers": auto_without_numbers,
            "large_mark": large_mark,
            "thin_mark": thin_mark,
        }

        return Response(response, status=200)

    def get_oldest_and_newest_cars(self):
        """Поиск в БД самого нового и самого старого автомобиля. Поиск произвожится по параметру year_of_issue"""

        try:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT MIN (year_of_issue), MAX (year_of_issue) FROM api_auto WHERE year_of_issue IS NOT NULL")
            oldest_and_newest_car = cursor.fetchone()
            oldest_car = oldest_and_newest_car[0]
            newest_car = oldest_and_newest_car[1]
        except:
            oldest_car = "no data"
            newest_car = "no data"
        finally:
            cursor.close()

        return oldest_car, newest_car

    def get_large_and_thim_marks(self):
        """Поиск самой многочисленной и малочисленной марки авто в БД"""

        try:
            # Формируем сгруппированный список из mark и количества,
            # Сортируем по количеству, и используем первое и последне значение
            number_of_cars_of_each_mark = Auto.objects.values('mark').annotate(dcount=Count('mark')).order_by('dcount')
            large_mark = number_of_cars_of_each_mark.last().get("mark")
            thin_mark = number_of_cars_of_each_mark.first().get("mark")
        except:
            large_mark = "no data"
            thin_mark = "no data"

        return thin_mark, large_mark
