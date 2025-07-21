from abc import ABC, abstractmethod
import threading

import JsonHandler
import Params


class BaseTestCase(ABC):
    def __init__(self, testName, serialSim):
        Params.DEVICE_ID = "abcd"  # Set the default device name, this should to be changed later with the input
        self.testName = testName
        self.serialSim = serialSim
        Params.SIMULATE_DELAY = False  # Resets to false by default.

    def getTestName(self):
        return self.testName

    @abstractmethod
    def set_params(self):
        pass

    @abstractmethod
    def run_test(self):
        pass

    # Helper functions that Test Cases can utilise.
    def promptForNonDefaultDeviceID(self):
        """This takes a unique, 4 hexadecimal character long device ID"""
        deviceID = "abcd"
        node_history_list_of_dictionaries = JsonHandler.load_from_json()
        is_device_id_not_unique = True
        while is_device_id_not_unique:
            deviceID = ""
            device_id_values = [d["DEVICE_ID"] for d in node_history_list_of_dictionaries]
            is_device_id_not_unique = False
            while len(deviceID) != 4:
                deviceID = input("Enter Custom DeviceID (4 hexadecimal characters): ")
                try:
                    deviceID_int = int(deviceID, 16)
                except ValueError:
                    print("Invalid DeviceID")
                    is_device_id_not_unique = True
            if deviceID in device_id_values:
                is_device_id_not_unique = True
                print("Please provide a Unique Device ID. Already existing ID's are listed below...")
                print(' '.join(map(str, device_id_values)))
                print()
        Params.DEVICE_ID = deviceID

    def run_thread_read_from_port(self):
        thread_read_from_port = threading.Thread(target=self.serialSim.read_from_port, args=(self.serialSim.ser,))
        thread_read_from_port.start()

    def run_thread_nbr_info(self):
        thread_nbr_info = threading.Thread(target=self.serialSim.nbr_info, args=(self.serialSim.ser,))
        thread_nbr_info.start()

    def run_thread_read_from_terminal(self):
        thread_read_from_terminal = threading.Thread(target=self.serialSim.read_from_terminal,
                                                     args=(self.serialSim.ser,))
        thread_read_from_terminal.start()
