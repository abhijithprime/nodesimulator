import Params
from Params import SensorVariant
import time
import threading
from .BaseTestCase import BaseTestCase


class NetworkTest_UIBurst_TestCase(BaseTestCase):
    def set_params(self):
        Params.DEVICE_TYPE = "beam_vw"
        Params.MAX_SENSORS = 1
        Params.SENSOR_TYPE = SensorVariant.VIBRATING_WIRE

    def custom_nbr_info(self):
        rssi = -999
        while True:
            reply = "nbr_info aaaa node NA NA " + str(rssi) + "\r\n"
            self.serialSim.serial_write_log_and_print(reply)
            rssi += 1

            reply = "nbr_info bbbb node NA NA " + str(rssi) + "\r\n"
            self.serialSim.serial_write_log_and_print(reply)
            rssi += 1

            reply = "nbr_info cccc node NA NA " + str(rssi) + "\r\n"
            self.serialSim.serial_write_log_and_print(reply)
            rssi += 1

            reply = "nbr_info dddd node NA NA " + str(rssi) + "\r\n"
            self.serialSim.serial_write_log_and_print(reply)
            rssi += 1

            reply = "nbr_info eeee node NA NA " + str(rssi) + "\r\n"
            self.serialSim.serial_write_log_and_print(reply)
            rssi += 1

            reply = "nbr_info ffff node NA NA " + str(rssi) + "\r\n"
            self.serialSim.serial_write_log_and_print(reply)
            rssi += 1

            time.sleep(0.5)
            if rssi > 999: rssi = -999

    def run_test(self):
        thread_custom_nbr_info = threading.Thread(target=self.custom_nbr_info, args=())
        thread_custom_nbr_info.start()
