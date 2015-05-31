import json
from django.contrib.auth.models import User
from django.db import models
from ethereum.abi import ContractTranslator
from blockchain.jsonrpc.ethereum import EthereumAPI

__author__ = 'nikolas'

class SensorDataManager(models.Manager):

    def last_record_or_false(self, sensor):
        last_record = self.get_queryset().filter(sensor=sensor).order_by("-timestamp")
        if not last_record:
            return False
        return last_record[0]


class Owner(models.Model):

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
            "gasPrice": 1000,
            "value": 0,
            "data": self.contract_code_lll
        }
        result = json_rpc.send_transaction(**params)
        if isinstance(result, str) and result.startswith("0x"):
            self.contract_deployed = True
            self.contract_addr = result
            self.save()

        abi = json.loads(self.contract_abi)

        for i, entity in enumerate(abi):
            if entity['type']  == 'constructor':
                del(abi[i])

        raw = json.dumps(abi)
        translator = ContractTranslator(raw.encode("utf-8"))

        a = translator.encode("sensors", [1])
        pass

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

    def __str__(self):
        return "<{}>: {}".format(self.owner.name, self.name)

    class Meta:
        app_label = "common"


class SensorData(models.Model):

    sensor = models.ForeignKey(Sensor, related_name="data")
    timestamp = models.DateTimeField(db_index=True)
    value = models.FloatField()

    objects = SensorDataManager()

    class Meta:
        app_label = "common"
