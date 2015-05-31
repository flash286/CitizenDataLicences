from client.entity.humidity import HumiditySensor
from client.entity.temperature import TemperatureSensor
from client.transport import BlockChainTransport

__author__ = 'nikolas'

class Worker(object):

    type_sensors = [TemperatureSensor, HumiditySensor]
    transport = BlockChainTransport

    data = {}

    def __init__(self):
        self.bc_channel = BlockChainTransport()
        for type_of_sensor in self.type_sensors:
            self.data[type_of_sensor.name] = type_of_sensor()

    def sync_with_blockchain(self):
        pass

    def get_data_by_sensor(self, sensor_cls, interval=False):
        sensor = self.data[sensor_cls.name]
        set_of_data = sensor.read_data_from_db(interval)
        for block_of_data in set_of_data:
            hash_id = self.bc_channel.send_to_buffer(sensor.name, block_of_data.data, block_of_data.ts)
            self.bc_channel.send_to_manager(sensor.name, block_of_data.ts, hash_id)
