import datetime
from django.core.management import BaseCommand
from ethereum.keys import sha3
from blockchain.entity import Contract
from common import Sensor, Transaction
import hashlib

__author__ = 'nikolas'


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--sensor_id',
                            dest='sensor',
                            help='Sensor PK')

    def handle(self, sensor, *args, **options):
        try:
            sensor = Sensor.objects.get(pk=sensor)
        except Sensor.DoesNotExist:
            self.stderr.write("Sensor not found")
            exit(1)
            return

        dt_start = datetime.datetime.utcnow()
        dt_end = dt_start + datetime.timedelta(seconds=10)

        dt_start = int(dt_start.replace(tzinfo=datetime.timezone.utc).timestamp())
        dt_end = int(dt_end.replace(tzinfo=datetime.timezone.utc).timestamp())

        contract = sensor.owner.contract_object
        contract.transact(sensor.owner.block_chain_account, 'holdTransaction', sensor.pk, dt_start, dt_end, value=10 ** 3)

        while True:
            transaction = contract.call(sensor.owner.block_chain_account, 'transactions', sensor.owner.block_chain_account[2:])
            if transaction[0].decode("ascii") == sensor.owner.block_chain_account[2:]:
                self.stdout.write("Transaction: {} found!".format(str(transaction)))
                transaction = Transaction.objects.create(
                    hash_id=str(transaction[4]),
                    dt_start=transaction[1],
                    dt_end=transaction[2],
                    cost=transaction[3],
                    status=1
                )
                break
