import Params
from Params import SensorVariant
from .BaseTestCase import BaseTestCase


class SoilInstrument_WithDelay_TestCase(BaseTestCase):
    def set_params(self):
        Params.DEVICE_TYPE = "beam_dg"
        Params.MAX_SENSORS = 5
        Params.SENSOR_TYPE = SensorVariant.SOIL_INSTRUMENTS
        Params.SIMULATE_DELAY = True
        # Params.SENSOR_ADDRESS = ["3450-0", "3451-1", "3452-2", "3453-3", "3454-4"]

    def run_test(self):
        self.run_thread_read_from_port()
