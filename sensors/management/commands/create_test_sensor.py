from common import Sensor, Owner

__author__ = 'nikolas'

from django.core.management import BaseCommand


class Command(BaseCommand):
    test_sensors = ["Temperature"]

    def add_arguments(self, parser):
        parser.add_argument('--owner',
                            dest='owner',
                            help='Owner user name')

    def handle(self, *args, **options):

        try:
            owner = Owner.objects.get(user__username=options['owner'])
        except Owner.DoesNotExist:
            self.stderr.write("Owner does not exists.")
            exit(1)
            return

        for test_sensor in self.test_sensors:
            sensor = Sensor.objects.create(
                owner=owner,
                name=test_sensor,
                description=test_sensor
            )
            self.stdout.write("Created: {}".format(sensor))
