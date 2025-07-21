import Params
from Params import SensorVariant
from .BaseTestCase import BaseTestCase


class BeamDG_GeoSense_TestCase(BaseTestCase):
    def set_params(self):
        Params.DEVICE_TYPE = "beam_dg"
        Params.MAX_SENSORS = 50
        Params.SENSOR_TYPE = SensorVariant.GEOSENSE_IPTM

    def run_test(self):
        self.run_thread_read_from_port()
