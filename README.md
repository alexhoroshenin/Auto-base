Описание разработки


Разработчик (junior): 	Алексей Хорошенин

Функционал приложения:
- Вывод списка с возможность сортировки
- Вывод отдельной записи
- Добавление записи
- Удаленние записи
- Вывод статистики

Язык:	Python

Фреймворк веб-приложения:	Django

Фреймворк REST API:	Django REST framework

База данных:	PostgreSQL

Способы тестирования:	unittest

Frontend:	bootstrap

Методы API для работы со справочником:

Общая информация
В справочнике хранится информация об автомобилях.
У каждого автомобиля есть поля с информацией:

car_number - Номер автомобиля
vin_code - VIN-код. Уникальный номер для каждого авто. Поле обязательное.
color - Цвет
mark - Марка
year_of_issue - Год выпуска
creating_date - Дата создания записи в справочнике. Поле заполняется автоматически.

Методы работы с API

1. Вывод списка

Чтобы получить список записей справочника сформируйте пустой GET-запрос по адресу: http//:host_ip/api/

Или перейдите по ссылке http//:host_ip/api/

Ответ сервера

200 OK


        {
            "auto": [
                    {
            "car_number": "DB808T",
            "vin_code": "BKO724693041YE",
            "color": "['зеленый']",
            "mark": "['Tesla']",
            "year_of_issue": 1993
        },
        {
            "car_number": "MO405X",
            "vin_code": "YCM731026813YD",
            "color": "['желтый']",
            "mark": "['Peugeot']",
            "year_of_issue": 1994
        },
        .............
        
2. Сортировка списка
Для сортировки списка укажите параметр GET-запроса, по которому нужно сортировать данные.

http://host_ip/api/?order_by=parametr_name

Сортировка доступна по всем параметрам: car_number, vin_code, color, mark, year_of_issue, creating_date.

Пример запроса с сортировкой по дате выпуска:

http//:host_ip/api/?order_by=year_of_issue

Обратите внимание, если параметр указан неверно, то сортировка произведена не будет.


3. Вывод информации по конкретному автомобилю
Чтобы получить информацию по конкретному автомобилю, укажите его vin_code в url-адресе

GET http//:host_ip/api/vin_code


Ответ сервера

200 OK


        {
            "auto":
                {
                    "car_number": "n12",
                    "vin_code": "123456789",
                    "color": "green",
                    "mark": "toyota",
                    "year_of_issue": 2002
                }
        }
        
Если vin_code в справочнике отсуствует, будет отправлено сообщение об ошибке.

404 Not Found


        {
            "message": "Object with vin_code 11212 not exist"
        }
        
2.3 Добавление автомобиля
Для добавления автомобиля в справочник используйте POST-запрос.

Обратите внимание, что поле vin_code обязательно для заполнения. Остальные поля необязательные.

Пример:

POST http//:host_ip/api/


        {
            "auto":
            {
                "car_number": " n12",
                "vin_code": "123456789", <<<< обязательное поле
                "color": "green",
                "mark": "toyota",
                "year_of_issue": "2002"

            }
        }
        
Ответ сервера:

201 Created


        {
            "message": "auto created successfully"
        }
        
Если не заполнено поле vin_code

400 Bad Request


        {
            "vin_code": [
        "This field is required."
        ],
        }
        
Если автомобиль с таким vin_code уже существует, информация добавлена не будет.

400 Bad Request


        {
            "message": "auto with vin code YOUR_VIN_CODE exists"
        }
        
4. Удаление автомобиля
Для удаления автомобиля используйте DELETE-запрос с vin_code удаляемого автомобиля в JSON-формате.

DELETE http//:host_ip/api/


        {
            "vin_code": "123456789"
        }
        
Ответ сервера в случае успешного удаления:

204 No Content


        {
            "message": "Auto with vin_code `123456789` has been deleted."
        }
        
Если автомобиля с таким vin_code не существовало, ответ будет следующим.

404 Not Found


        {
            "message": "Auto with vin_code `YOUR_VIN_CODE` not exist."
        }
        
5. Статистика справочника
Чтобы получить общую статистику справочника перейдите по ссылке http://host_ip/api/statistics

Или отправьте GET-запрос по этому же адресу.

count_auto - количество авто в справочнике
first_created_object_data - дата создания первой записи
last_created_object_data - дата создания последней записи
oldest_car - самый старый автомобиль в списке
newest_car - самый новый
auto_without_numbers - авто, у которых нет номерных знаков
large_mark - самая многочисленная марка
thin_mark - самая малочисленная марка


Ответ сервера

200 OK


{
    "count_auto": 21,
    "first_created_object_data": "2020-06-09T10:47:33.007240Z",
    "last_created_object_data": "2020-06-09T11:27:07.724483Z",
    "oldest_car": 1985,
    "newest_car": 2020,
    "auto_without_numbers": 0,
    "large_mark": "['Renault']",
    "thin_mark": "['Lada']"
}
