from datetime import timezone
import json

from django.contrib.auth.models import User

from django.db import models

from blockchain.entity import Contract
from blockchain.jsonrpc.ethereum import EthereumAPI

__author__ = 'nikolas'


class SensorDataQS(models.QuerySet):
    def create(self, **kwargs):
        sensor = kwargs['sensor']
        owner = sensor.owner
        contract = owner.contract_object
        ts = int(kwargs['timestamp'].replace(tzinfo=timezone.utc).timestamp())
        first_data = kwargs.pop("first_data", False)
        if first_data:
            contract.transact(owner.block_chain_account, "createSensor", sensor.id, sensor.fee, ts)
        else:
            contract.transact(owner.block_chain_account, "createData", sensor.id, ts)
        super(SensorDataQS, self).create(**kwargs)


class SensorDataManager(models.Manager):
    def get_queryset(self):
        return SensorDataQS(self.model, using=self._db)

    def last_record_or_false(self, sensor):
        last_record = self.get_queryset().filter(sensor=sensor).order_by("-timestamp")
        if not last_record:
            return False
        return last_record[0]


class Owner(models.Model):
    CONTRACT_REPR = Contract

    _contract_obj = None

    user = models.OneToOneField(User)
    name = models.CharField(max_length=255)
    balance = models.FloatField()
    block_chain_account = models.CharField(max_length=255)
    contract_code_lll = models.TextField()
    contract_code_pretty = models.TextField()
    contract_name = models.CharField(max_length=255, default="")
    contract_abi = models.TextField(default="")
    contract_deployed = models.BooleanField(default=False)
    contract_addr = models.CharField(max_length=255, default="")

    @property
    def contract_object(self):

        assert len(self.contract_code_pretty) > 0

        if not self.contract_abi:
            self.compile_contract()

        if not self.contract_addr or not self.contract_deployed:
            self.deploy_contract()

        if not self._contract_obj or not isinstance(self._contract_obj, self.CONTRACT_REPR):
            self._contract_obj = Contract(self.contract_addr, self.contract_abi)

        return self._contract_obj

    @property
    def blockchain_balance(self):
        balance = self.contract_object.balance(self.block_chain_account)
        self.balance = balance
        self.save()
        return balance

    @property
    def contract_balance(self):
        return self.contract_object.balance()

    def compile_contract(self):
        json_rpc = EthereumAPI()
        result = json_rpc.compile_solidity(self.contract_code_pretty)
        self.contract_code_lll = result[self.contract_name]['code']
        self.contract_abi = json.dumps(result[self.contract_name]['info']['abiDefinition'])
        self.save()

    def deploy_contract(self):
        if not self.contract_code_lll:
            self.compile_contract()
        json_rpc = EthereumAPI()
        params = {
            "from_addr": self.block_chain_account,
            "to_addr": "",
            "gas": 1000000,
            "gasPrice": 10000000000000,
            "value": 0,
            "data": self.contract_code_lll
        }

        if not self.contract_deployed:
            result = json_rpc.send_transaction(**params)
            self.contract_deployed = True
            self.contract_addr = result
            self.save()

    @property
    def python_contract_abi(self):
        return json.loads(self.contract_abi)

    def update_balance(self):
        json_rpc = EthereumAPI()
        balance = json_rpc.balance_at(self.block_chain_account)
        print(balance)

    def __str__(self):
        return "{}:<{}>".format(self.name, self.block_chain_account)

    class Meta:
        app_label = "common"


class Transaction(models.Model):
    statuses = (
        (1, "HOLD"),
        (2, "SUCCESS"),
        (3, "FAIL"),
        (4, 'OUT_OF_DATE')
    )

    hash_id = models.CharField(max_length=255)
    cost = models.PositiveIntegerField(default=0)
    status = models.PositiveSmallIntegerField(choices=statuses, default=1)
    dt_start = models.PositiveIntegerField(default=0)
    dt_end = models.PositiveIntegerField(default=0)

    class Meta:
        app_label = "common"


class Sensor(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(default="")
    owner = models.ForeignKey(Owner, related_name="sensors")
    fee = models.PositiveIntegerField(default=0)

    def blockchain_value(self):
        contract = self.owner.contract_object
        result = contract.call(self.owner.block_chain_account, 'sensors', self.pk)
        return {
            "dt_start": result[1],
            "dt_end": result[2],
            "fee": result[3]
        }

    def __str__(self):
        return "<{}>: {}".format(self.owner.name, self.name)

    def data_dt_start(self):
        data = self.data.order_by('timestamp').first()
        if not data:
            return 0
        return data.timestamp

    def data_dt_end(self):
        data = self.data.order_by('-timestamp').first()
        if not data:
            return 0
        return data.timestamp

    class Meta:
        app_label = "common"


class SensorData(models.Model):
    sensor = models.ForeignKey(Sensor, related_name="data")
    timestamp = models.DateTimeField(db_index=True)
    value = models.FloatField()

    objects = SensorDataManager()

    @property
    def unix_timestamp(self):
        return self.timestamp.replace(tzinfo=timezone.utc).timestamp()

    class Meta:
        app_label = "common"
