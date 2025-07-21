import Params
from Params import SensorVariant
import time
import threading
from .BaseTestCase import BaseTestCase


class NetworkTest_Range_TestCase(BaseTestCase):
    def set_params(self):
        Params.DEVICE_TYPE = "beam_vw"
        Params.MAX_SENSORS = 1
        Params.SENSOR_TYPE = SensorVariant.VIBRATING_WIRE

    def custom_nbr_info(self):
        while True:
            # Testing full ranges of the diff levels
            reply = "nbr_info aaaa node NA NA -80\r\n"
            self.serialSim.serial_write_log_and_print(reply)

            reply = "nbr_info bbbb node NA NA -81\r\n"
            self.serialSim.serial_write_log_and_print(reply)

            reply = "nbr_info cccc node NA NA -90\r\n"
            self.serialSim.serial_write_log_and_print(reply)

            reply = "nbr_info dddd node NA NA -91\r\n"
            self.serialSim.serial_write_log_and_print(reply)

            reply = "nbr_info eeee node NA NA -100\r\n"
            self.serialSim.serial_write_log_and_print(reply)

            reply = "nbr_info ffff node NA NA -101\r\n"
            self.serialSim.serial_write_log_and_print(reply)

            time.sleep(5)

    def run_test(self):
        thread_custom_nbr_info = threading.Thread(target=self.custom_nbr_info, args=())
        thread_custom_nbr_info.start()
