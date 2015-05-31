import datetime
import random
from django.core.management import BaseCommand
from common import Sensor, SensorData

__author__ = 'nikolas'


class Command(BaseCommand):

    def handle(self, *args, **options):
        data_range = lambda : random.randint(-30, 30)
        sensors = Sensor.objects.all()
        self.stdout.write("Available sensors: {}".format(sensors))
        start_time = datetime.datetime.utcnow()
        for sensor in sensors:
            last_record = SensorData.objects.last_record_or_false(sensor)
            if last_record:
                print(last_record.timestamp)
                start_time = last_record.timestamp + datetime.timedelta(seconds=1)
            for interval in range(1, 100):
                dt = start_time + datetime.timedelta(seconds=interval * 60)
                value = data_range()
                SensorData.objects.create(
                    sensor=sensor,
                    timestamp=dt,
                    value=value
                )
                self.stdout.write("For {} add record: <{}: {}>".format(sensor, dt, value))