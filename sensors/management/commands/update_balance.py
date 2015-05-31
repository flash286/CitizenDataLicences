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

        owner.update_balance()
        self.stdout.write("<{}> Balance: {}".format(owner.balance))
