import JsonHandler
import Params
from Params import SensorVariant
from .BaseTestCase import BaseTestCase
import Log


def set_parameters_helper_func():
    """Takes inputs and returns deviceType, maxSensors, sensorTypeInt.
    This function is used for both making a custom testcase and saving a new testcase"""
    deviceTypes = [
        "beam_an",
        "beam_dg",
        # "beam_rl", # SKY is beam_rn but in device info it's beam_rl
        "beam_tm", # Only SISGEO_TILT_METER
        "beam_vw",
    ]
    selectedDeviceType = ""
    while len(selectedDeviceType) < 1:
        for i in range(len(deviceTypes)):
            print("\t", str(i) + ".", deviceTypes[i])

        inputStr: str = input("Please select device type: ")
        try:
            inputInt = int(inputStr)
            if len(deviceTypes) > inputInt >= 0:
                selectedDeviceType = deviceTypes[inputInt]
                Log.LogAndPrint("Device Type " + selectedDeviceType + " is selected")
        except ValueError:
            pass
    Params.DEVICE_TYPE = selectedDeviceType

    maxSensors: int = -1
    while maxSensors < 1:
        if selectedDeviceType == "beam_an":
            inputStr = input("State maximum number of sensors (BEAM-AN : 1 or 4) : ")
            try:
                maxSensors = int(inputStr)
                if not (maxSensors == 1 or maxSensors == 4):
                    print("Invalid number of sensors provided\n")
                    maxSensors = - 1
            except ValueError:
                pass
        elif selectedDeviceType == "beam_tm":
            print("SISGEO_TILT_METER is selected with ONE sensor")
            maxSensors = 1
        elif selectedDeviceType == "beam_vw":
            inputStr = input("State maximum number of sensors (BEAM-VW : 1 or 8) : ")
            try:
                maxSensors = int(inputStr)
                if not (maxSensors == 1 or maxSensors == 8):
                    print("Invalid number of sensors provided")
                    maxSensors = - 1
            except ValueError:
                pass
        else:
            inputStr = input("State maximum number of sensors: ")
            try:
                maxSensors = int(inputStr)
            except ValueError:
                pass
    Params.MAX_SENSORS = maxSensors

    sensorTypeInt: int = -1
    while sensorTypeInt < 0:
        if selectedDeviceType == "beam_tm":
            sensorTypeInt = 30
            Params.SENSOR_TYPE = SensorVariant(sensorTypeInt)
            continue
        print("Test Sensors: ")
        for enum in SensorVariant:
            if SensorVariant.isSensorTestDevice(enum):
                print('\t', str(enum.value) + ".", enum.name)
        print(Params.DEVICE_TYPE + " sensors: ")
        for enum in SensorVariant:
            if SensorVariant.isSensorOfDeviceType(enum, Params.DEVICE_TYPE):
                print('\t', str(enum.value) + ".", enum.name)

        inputStr = input("Select sensor variant: ")
        try:
            sensorTypeInt = int(inputStr)
            Params.SENSOR_TYPE = SensorVariant(
                sensorTypeInt)  # throws ValueError if can't find enum with matching value
        except ValueError:
            sensorTypeInt = -1

        if sensorTypeInt == 27 or sensorTypeInt == 29 or sensorTypeInt == 35 or sensorTypeInt == 36 or sensorTypeInt == 37 or sensorTypeInt == 42 or sensorTypeInt == 43:
            sensor_addresses_input = SensorVariant.checkToGetTheSensorAddresses(Params.SENSOR_TYPE, Params.MAX_SENSORS)
            if sensor_addresses_input != -1:
                Params.SENSOR_ADDRESS = sensor_addresses_input
                print("SENSOR ADDRESS", Params.SENSOR_ADDRESS)
    return selectedDeviceType, maxSensors, sensorTypeInt


class Custom_TestCase(BaseTestCase):
    def set_params(self):
        selectedDeviceType, maxSensors, sensorTypeInt = set_parameters_helper_func()

        super().promptForNonDefaultDeviceID()

        Log.LogAndPrint(
            "CUSTOM TEST configured: Device ID - {}\tDevice Type - {}\tMax Sensors - {}\tSensor Type -[{}] {}".format(
                Params.DEVICE_ID, selectedDeviceType, maxSensors, Params.SENSOR_TYPE.value, Params.SENSOR_TYPE.name))

        node_history_list_of_dictionaries = JsonHandler.load_from_json()
        node_history_list_of_dictionaries.append(
            {"DEVICE_TYPE": str(selectedDeviceType), "MAX_SENSORS": int(maxSensors),
             "SENSOR_TYPE_INT": int(sensorTypeInt), "DEVICE_ID": Params.DEVICE_ID, "SENSOR_ADDRESS": Params.SENSOR_ADDRESS})
        JsonHandler.save_to_json(node_history_list_of_dictionaries)
        Log.LogAndPrint(
            "Test Saved Successfully: Device ID - {}\tDevice Type - {} \tMax Sensors - {}\tSensor Type - [{}] "
            "{}".format(Params.DEVICE_ID, selectedDeviceType, maxSensors, Params.SENSOR_TYPE.value,
                        Params.SENSOR_TYPE.name))

    def run_test(self):
        self.run_thread_read_from_port()
