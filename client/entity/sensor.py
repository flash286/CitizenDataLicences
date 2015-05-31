__author__ = 'nikolas'

class Sensor(object):

    name = 'sensor'

    f_db = "/tmp/sensors/{}".format(name)

    def __init__(self):
        self.f_stream = open(self.f_db, "r")

    def write_block_data(self, data, dt):
        pass

    def read_data_from_db(self, interval=False):
        pass