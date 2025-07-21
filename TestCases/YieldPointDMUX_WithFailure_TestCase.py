import Params
from Params import SensorVariant
from .BaseTestCase import BaseTestCase


class YieldPointDMUX_WithFailure_TestCase(BaseTestCase):
    def set_params(self):
        Params.DEVICE_TYPE = "beam_dg"
        Params.MAX_SENSORS = 4
        Params.SENSOR_TYPE = SensorVariant.YIELDPOINT_DMUX
        Params.SIMULATE_FAILURE_GET_ADDRESS = True

    def run_test(self):
        self.run_thread_read_from_port()
