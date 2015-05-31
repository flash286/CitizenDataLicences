import datetime
import random
from django.core.management import BaseCommand
from blockchain.jsonrpc.ethereum import EthereumAPI
from common import Sensor, SensorData, Owner

__author__ = 'nikolas'


class Command(BaseCommand):

    def handle(self, *args, **options):
        owner = Owner.objects.get(user__username="nikolas")
        rpc = EthereumAPI()
        self.stdout.write(str(rpc.storage_at(owner.contract_addr)))
