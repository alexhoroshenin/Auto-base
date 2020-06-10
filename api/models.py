from django.db import models


class Auto(models.Model):
    car_number = models.CharField(max_length=50, blank=True, null=True)
    vin_code = models.CharField(max_length=50)
    color = models.CharField(max_length=50, blank=True, null=True)
    mark = models.CharField(max_length=50, blank=True, null=True)
    year_of_issue = models.PositiveIntegerField(blank=True, null=True)
    creating_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return ('Автомобиль: ' + self.to_str(self.mark)
                + ' ' + self.to_str(self.car_number)
                + ' ' + self.to_str(self.vin_code)
                + ' ' + self.to_str(self.color)
                + ' ' + self.to_str(self.year_of_issue)
                )

    def to_str(self, param):
        """Проверка на наличие параметра. В случае отсутствия формируется пустая строка"""

        if not param:
            return ''
        else:
            return str(param)
