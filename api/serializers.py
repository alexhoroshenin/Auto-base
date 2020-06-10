from rest_framework import serializers
from .models import Auto

class AutoSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Auto
        fields = ['car_number', 'vin_code', 'color', 'mark', 'year_of_issue']

    def auto_exist(self, vin_code):

        if Auto.objects.filter(vin_code=vin_code).count() > 0:
            return True
        return False
