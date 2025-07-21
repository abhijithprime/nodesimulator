import Params
from Params import SensorVariant
from .BaseTestCase import BaseTestCase


class BeamAN_VW1_TestCase(BaseTestCase):
    def set_params(self):
        # VW1
        Params.DEVICE_TYPE = "beam_vw"
        Params.MAX_SENSORS = 1
        Params.SENSOR_TYPE = SensorVariant.VIBRATING_WIRE

    def run_test(self):
        self.run_thread_read_from_port()
