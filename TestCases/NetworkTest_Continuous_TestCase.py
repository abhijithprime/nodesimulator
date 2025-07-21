import Params
from Params import SensorVariant
import time
import threading
from .BaseTestCase import BaseTestCase


class NetworkTest_Continuous_TestCase(BaseTestCase):
    def set_params(self):
        Params.DEVICE_TYPE = "beam_vw"
        Params.MAX_SENSORS = 1
        Params.SENSOR_TYPE = SensorVariant.VIBRATING_WIRE

    def custom_nbr_info(self):
        counter = 0
        reply = ""
        rssi = -999
        while True:
            nodeId = 0x5a50 + counter
            counter += 1
            if counter > 5: counter = 0

            reply = "nbr_info " + str(hex(nodeId))[2:] + " node NA NA " + str(rssi) + "\r\n"
            rssi += 1
            if rssi > 999: rssi = -999

            self.serialSim.serial_write_log_and_print(reply)
            time.sleep(0.05)

    def run_test(self):
        thread_custom_nbr_info = threading.Thread(target=self.custom_nbr_info, args=())
        thread_custom_nbr_info.start()
