import Params
from Params import SensorVariant
from .BaseTestCase import BaseTestCase


class BeamRN_TestCase(BaseTestCase):
    def set_params(self):
        # VW1
        Params.DEVICE_TYPE = "beam_rl"
        Params.MAX_SENSORS = 0
        Params.SENSOR_TYPE = SensorVariant.SENSOR_DUMMY
        Params.DEVICE_ID = "9f9d"

    def run_test(self):
        self.run_thread_read_from_port()
