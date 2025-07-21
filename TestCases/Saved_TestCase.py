import JsonHandler
import Params
from Params import SensorVariant
from .BaseTestCase import BaseTestCase
from .Custom_TestCase import set_parameters_helper_func
import Log


class Load_Saved_TestCase(BaseTestCase):
    def __init__(self, testName, serialSim):
        super().__init__(testName, serialSim)
        self.IsTestCaseCorrectlyLoaded = None

    def set_params(self):
        """This method is used for regular use in normal mode"""
        node_history_list_of_dictionaries = JsonHandler.load_from_json()
        device_history_index = 0
        self.IsTestCaseCorrectlyLoaded = True

        if len(node_history_list_of_dictionaries) <= 0:
            Log.LogAndPrint("\nNo Saved Test Cases. Please proceed with a CUSTOM test case or add a new test case.")
            self.IsTestCaseCorrectlyLoaded = False
            return
        device_history_index: int = -1
        while device_history_index < 0:
            print()
            for i in range(len(node_history_list_of_dictionaries)):
                print("\t", str(i) + ".",
                      "Device ID :", node_history_list_of_dictionaries[i]["DEVICE_ID"],
                      "\tDevice Type :", node_history_list_of_dictionaries[i]["DEVICE_TYPE"],
                      "\tMax Sensors :", node_history_list_of_dictionaries[i]["MAX_SENSORS"],
                      "\tSensor Type Integer :",
                      SensorVariant(int(node_history_list_of_dictionaries[i]["SENSOR_TYPE_INT"])))

            inputStr: str = input("\nPlease select a saved node : ")
            try:
                inputInt = int(inputStr)
                if len(node_history_list_of_dictionaries) > inputInt >= 0:
                    device_history_index = inputInt
            except ValueError:
                pass
        selected_saved_device = node_history_list_of_dictionaries[device_history_index]

        selectedDeviceType = selected_saved_device["DEVICE_TYPE"]
        Params.DEVICE_TYPE = selectedDeviceType

        maxSensors = selected_saved_device["MAX_SENSORS"]
        Params.MAX_SENSORS = maxSensors

        sensor_address = selected_saved_device["SENSOR_ADDRESS"]
        Params.SENSOR_ADDRESS = sensor_address

        try:
            sensor_type_int = int(selected_saved_device["SENSOR_TYPE_INT"])
            print("\n\nSensor type :", SensorVariant(sensor_type_int))
            Params.SENSOR_TYPE = SensorVariant(
                sensor_type_int)  # throws ValueError if it can't find enum with matching value
        except ValueError:
            print("\n\nError occurred at assigning sensor type\n\n")
            pass

        deviceID = selected_saved_device["DEVICE_ID"]
        Params.DEVICE_ID = deviceID

        Log.LogAndPrint(
            "SAVED TEST loaded: Device ID - {}\tDevice Type - {}\tMax Sensors - {}\tSensor Type -[{}] {}".format(
                Params.DEVICE_ID, selectedDeviceType, maxSensors, Params.SENSOR_TYPE.value, Params.SENSOR_TYPE.name))
        Log.LogAndPrint("Sensor Addresses - " + str(Params.SENSOR_ADDRESS))

    def set_arg_params(self, device_id):
        """This method is called only in the parameter mode. This takes device_ID which was given as a parameter as an input and loads the other parameters.
        Returns -1 is the Device ID is not an already saved device, 0 if everything is correct"""
        node_history_list_of_dictionaries = JsonHandler.load_from_json()
        device_history_index = 0
        self.IsTestCaseCorrectlyLoaded = False
        device_id_values = [d["DEVICE_ID"] for d in node_history_list_of_dictionaries]

        while not self.IsTestCaseCorrectlyLoaded:
            try:
                device_history_index = device_id_values.index(device_id)
                self.IsTestCaseCorrectlyLoaded = True
            except ValueError:
                print("Please provide a correct Device ID. Existing ID's are listed below...")
                if len(device_id_values) == 0:
                    print("\tNo saved Device ID's available")
                print(' '.join(map(str, device_id_values)))
                print()
                return -1

        selected_saved_device = node_history_list_of_dictionaries[device_history_index]

        selectedDeviceType = selected_saved_device["DEVICE_TYPE"]
        Params.DEVICE_TYPE = selectedDeviceType

        maxSensors = selected_saved_device["MAX_SENSORS"]
        Params.MAX_SENSORS = maxSensors

        sensor_address = selected_saved_device["SENSOR_ADDRESS"]
        Params.SENSOR_ADDRESS = sensor_address

        sensor_type_int: int = -1
        try:
            sensor_type_int = int(selected_saved_device["SENSOR_TYPE_INT"])
            Params.SENSOR_TYPE = SensorVariant(
                sensor_type_int)  # throws ValueError if it can't find enum with matching value
        except ValueError:
            print("\n\nError occurred at assigning sensor type\n\n")
            pass

        deviceID = selected_saved_device["DEVICE_ID"]
        Params.DEVICE_ID = deviceID

        Log.LogAndPrint(
            "SAVED TEST loaded: Device ID - {}\tDevice Type - {}\tMax Sensors - {}\tSensor Type -[{}] {}".format(
                Params.DEVICE_ID, selectedDeviceType, maxSensors, Params.SENSOR_TYPE.value, Params.SENSOR_TYPE.name))
        Log.LogAndPrint("Sensor Addresses - " + str(Params.SENSOR_ADDRESS))
        return 0

    def run_test(self):
        if self.IsTestCaseCorrectlyLoaded:
            self.run_thread_read_from_port()


class Save_New_TestCase(BaseTestCase):
    def set_params(self):
        selectedDeviceType, maxSensors, sensorTypeInt = set_parameters_helper_func()

        super().promptForNonDefaultDeviceID()

        node_history_list_of_dictionaries = []
        node_history_list_of_dictionaries = JsonHandler.load_from_json()
        node_history_list_of_dictionaries.append(
            {"DEVICE_TYPE": str(selectedDeviceType), "MAX_SENSORS": int(maxSensors),
             "SENSOR_TYPE_INT": int(sensorTypeInt), "DEVICE_ID": Params.DEVICE_ID,
             "SENSOR_ADDRESS": Params.SENSOR_ADDRESS})
        JsonHandler.save_to_json(node_history_list_of_dictionaries)
        Log.LogAndPrint(
            "Test Saved Successfully: Device ID - {}\tDevice Type - {} \tMax Sensors - {}\tSensor Type - [{}] {}".format(
                Params.DEVICE_ID, selectedDeviceType, maxSensors, Params.SENSOR_TYPE.value, Params.SENSOR_TYPE.name))

    def run_test(self):
        # Not running anything
        pass


class Delete_TestCase(BaseTestCase):
    def set_params(self):
        node_history_list_of_dictionaries = []
        node_history_list_of_dictionaries = JsonHandler.load_from_json()
        device_id_values = [d["DEVICE_ID"] for d in node_history_list_of_dictionaries]

        node_to_delete_index: int = -1
        while node_to_delete_index < 0:
            print()
            for i in range(len(node_history_list_of_dictionaries)):
                print("\t",
                      "Device ID :", node_history_list_of_dictionaries[i]["DEVICE_ID"],
                      "\tDevice Type :", node_history_list_of_dictionaries[i]["DEVICE_TYPE"],
                      "\tMax Sensors :", node_history_list_of_dictionaries[i]["MAX_SENSORS"],
                      "\tSensor Type Integer :",
                      SensorVariant(int(node_history_list_of_dictionaries[i]["SENSOR_TYPE_INT"])))

            inputStr: str = input(
                "\nPlease select the Device ID of the Node to delete. Enter 'all' to delete all. Enter 'q' to quit : ")
            if inputStr == 'q':
                Log.LogAndPrint("Exiting the simulator")
                return
            if inputStr == 'all':
                while 1:
                    delete_all_choice_confirmation = str(input("Do you want to delete all (Y / N) ? "))
                    if delete_all_choice_confirmation.lower() == 'y':
                        Log.LogAndPrint("Deleting all saved entries...")
                        print("Exiting the program")
                        node_history_list_of_dictionaries = []
                        JsonHandler.save_to_json(node_history_list_of_dictionaries)
                        return
                    elif delete_all_choice_confirmation.lower() == 'n':
                        print("Exiting the program")
                        return
                    print("Please enter either 'y' or 'n'")
            try:
                node_to_delete_index = device_id_values.index(inputStr)
            except ValueError:
                print("Invalid Device ID. Please retry...")

        node_to_delete = node_history_list_of_dictionaries.pop(node_to_delete_index)
        JsonHandler.save_to_json(node_history_list_of_dictionaries)
        Log.LogAndPrint(
            "Node Deleted Successfully: Device ID - {}\tDevice Type - {} \tMax Sensors - {}\tSensor Type Int - {}".format(
                node_to_delete["DEVICE_ID"], node_to_delete["DEVICE_TYPE"], node_to_delete["MAX_SENSORS"],
                node_to_delete["SENSOR_TYPE_INT"]))

    def run_test(self):
        # Not running anything
        pass
