from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, reverse, redirect
from api.models import Auto
import random

def index(request):

    count_auto = Auto.objects.count()

    if request.method == 'POST':
        set_count = request.POST.get('set_count', '')
        try:
            set_count = int(set_count)
        except:
            return redirect('/?error={}'.format('Введите целое число'))

        if set_count and isinstance(set_count, int):

            create_test_set(set_count)
            return redirect('/?add_count={}'.format(set_count))


    if not count_auto:
        count_auto = 0


    context = {
        'count_auto': count_auto,
    }

    return render(request, 'auto_base/index.html', context)

def create_test_set(set_count):
    population_chars = 'ABCDEKMHOPCTYX'

    for i in range(set_count):
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

def delete(request):

    Auto.objects.all().delete()

    return redirect('/?message={}'.format('Все записи успешно удалены из справочника'))