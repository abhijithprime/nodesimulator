import Params
from Params import SensorVariant
from .BaseTestCase import BaseTestCase


class Measurand_TestCase(BaseTestCase):
    def set_params(self):
        Params.DEVICE_TYPE = "beam_dg"
        Params.MAX_SENSORS = 201
        Params.SENSOR_TYPE = SensorVariant.MEASURAND

    def run_test(self):
        self.run_thread_read_from_port()
