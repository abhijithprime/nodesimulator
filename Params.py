from enum import Enum


class SensorVariant(Enum):
    SENSOR_DUMMY = 0
    VIBRATING_WIRE = 1
    ANALOG_VOLTAGE = 2
    ANALOG_CURRENT = 3
    LDVT = 4
    WHEATSTONE_BRIDGE = 5
    SISGEO_DTilt = 6
    TEKBOK_TBSHT04 = 7
    GEOKON_6150E = 8
    GEOSENSE_IPTM = 9
    EAN_92MB = 10
    RST_TILT = 11
    SISGEO_BI_AXIAL = 16
    SISGEO_inclinometer = 17
    SISGEO_LoadCell = 18
    SISGEO_Piezometer = 19
    KR_DG = 20
    CAMPBELL_CS451 = 21
    MEASURAND = 22
    RAIN_GAUGE = 23
    CAMPBELL_CS650 = 24
    # 25 allocated to Virtual Sensor
    MEASURAND_SAATOP = 26  # Will consider as sub-sensor of Measurand can't activate alone.
    YIELDPOINT = 27
    ZC_IPI = 28
    YIELDPOINT_DMUX = 29
    SISGEO_TILT_METER = 30
    ENCARDIO_TILT_METER = 31
    GEOGAGE_TILT_METER = 32
    POTENTIOMETER = 33
    SDI12_GENERIC = 34
    MDT_SMART_LINK = 35
    DATATAKER = 36
    INSITU_AQUA_TROLL = 37
    VW_AND_PRESSURE = 38
    SISGEO_DIGITAL = 39
    SOIL_INSTRUMENTS = 40
    BSIL_RT_1030 = 41
    ESSEARTH_HIDCELL = 42
    ESSEARTH_YP = 43
    OSPREY_IPX = 44
    DG_DIAG_TEST = 96
    RS485_TEST = 97
    RS232_TEST = 98
    SDI12_TEST = 99
    MAX_SENSOR_SUPPORTED = 100

    def isSensorTestDevice(sensorVariant):
        sensorTypeID = sensorVariant.value
        match sensorTypeID:
            case 0 | 100 | 96 | 97 | 98 | 99:
                return True

        return False

    # TODO This was reversed engineered cause no documentation. Needs verification.
    def isSensorOfDeviceType(sensorVariant, type):
        if SensorVariant.isSensorTestDevice(sensorVariant):
            return False

        sensorTypeID = sensorVariant.value

        match sensorTypeID:
            case 2 | 3 | 4 | 5 | 33:
                return type == "beam_an"
            case 6 | 7 | 8 | 9 | 10 | 11 | \
                 16 | 17 | 18 | 19 | 20 | 21 | 22 | \
                 24 | \
                 26 | 27 | 28 | 29 | 30 | 31 | 32 | \
                 34 | 35 | 36 | 37 | \
                 39 | 40 | 41 | 42 | 43 | 44:
                return type == "beam_dg"
            case 1 | 23 | 38:
                return type == "beam_vw"
            case _:
                print("ERROR: sensor type " + sensorVariant.name + "(" + str(sensorTypeID) + ") not handled")

    def checkToGetTheSensorAddresses(sensorVariant, maxSensors):
        if maxSensors <= 0:
            SENSOR_ADDRESS = []
            return -1
        if sensorVariant == SensorVariant.MDT_SMART_LINK or sensorVariant == SensorVariant.YIELDPOINT or sensorVariant == SensorVariant.ESSEARTH_YP:
            maxSensors = 1
            print("Maximum number of sensors is set to 1")
        if sensorVariant == SensorVariant.YIELDPOINT or SensorVariant.YIELDPOINT_DMUX or SensorVariant.MDT_SMART_LINK or SensorVariant.DATATAKER or SensorVariant.INSITU_AQUA_TROLL or SensorVariant.ESSEARTH_HIDCELL or SensorVariant.ESSEARTH_YP:
            sensor_addresses_input = []
            while len(sensor_addresses_input) < maxSensors:
                sensor_addresses_input = input(
                    "Please enter " + str(maxSensors) + " addresses for sensors seperated by spaces: ").strip().split(
                    " ")
                if len(sensor_addresses_input) > maxSensors:
                    print("Try again with correct number of sensor addresses")
            return sensor_addresses_input


# Default Parameter Values. These should be changed in correct implementation
PORT = "/dev/ttyACM0"
BAUD = 115200
DEVICE_ID = "5612"
DEVICE_TYPE = "beam_dg"
VERSION = "5.2.25.0409"
MAX_SENSORS = "32"
FREQUENCY = "902000"
F_MIN = "902000"
F_MAX = "928000"
TX_POWER = "26"
IPI = "15"
NODE_INDEX = "0"
RELAY_STATUS = "0"
SECRET_KEY = "2b7e151628aed2a6abf7158809cf4f3c"
BATTERY = "3.5850V"
TIME = "1597127572"
NUM_OF_CHANNEL = 15
SENSOR_TYPE: SensorVariant = SensorVariant.VIBRATING_WIRE
SENSOR_ADDRESS = 0
CALIBRATION = {0: "1 374f07e5 c143d70a 41bb5c29 420149ba", 1: "1 3eddcc64 c143b22d 41454fdf bea60486"}
NUM_OF_SENSOR_CHANNEL = 9
MIN_SAMPLING_INTERVAL = 1
NETWORK_SIZE = 10
FLASH_RETRANSMISSION = 1

SIMULATE_DELAY: bool = False
SIMULATE_FAILURE_GET_ADDRESS: bool = False


def resetSimulateParams():
    SIMULATE_DELAY = False
    SIMULATE_FAILURE_GET_ADDRESS = False


""" Util Diagnosis """
util_diagnosis = {
    "beam_dg": [('batt_status', '1'),
                ('batt_value', '3.527000'),
                ('batt_unit', 'V'),
                ('env_sensor_status', '1'),
                ('env_sensor_id', '0x60'),
                ('temp_value', '26.400000'),
                ('temp_unit', 'C'),
                ('pressure_value', '101137.859375'),
                ('pressure_unit', 'Pa'),
                ('humidity_value', '97.231003'),
                ('humidity_unit', '%'),
                ('external_flash_status', '1'),
                ],
    "beam_an": [('batt_status', '1'),
                ('batt_value', '3.527000'),
                ('batt_unit', 'V'),
                ('env_sensor_status', '1'),
                ('env_sensor_id', '0x60'),
                ('temp_value', '26.400000'),
                ('temp_unit', 'C'),
                ('pressure_value', '101137.859375'),
                ('pressure_unit', 'Pa'),
                ('humidity_value', '97.231003'),
                ('humidity_unit', '%'),
                ('external_flash_status', '1'),
                ('ADC_status', '1'),
                ('adc_id1', '0x08'),
                ('adc_id2', '0x08')
                ],
    "beam_tm": [('batt_status', '1'),
                ('batt_value', '3.527000'),
                ('batt_unit', 'V'),
                ('env_sensor_status', '1'),
                ('env_sensor_id', '0x60'),
                ('temp_value', '26.400000'),
                ('temp_unit', 'C'),
                ('pressure_value', '101137.859375'),
                ('pressure_unit', 'Pa'),
                ('humidity_value', '97.231003'),
                ('humidity_unit', '%'),
                ('external_flash_status', '1'),
                ('ADC_status', '1'),
                ('adc_id1', '0x08'),
                ('adc_id2', '0x08')
                ],
    "beam_vw": [('BATTERY_TEST_STATUS', '1'),
                ('Battery_value', '3.593000'),
                ('Battery_unit', 'V'),
                ('BME_TEST_STATUS', '1'),
                ('BME_ID', '0x60'),
                ('TEMP', '26.559999'),
                ('TEMP_unit', 'C'),
                ('PRESSURE', '100875.804688'),
                ('PRESSURE_unit', 'Pa'),
                ('HUMIDITY', '36.254002'),
                ('HUMIDITY_unit', '%'),
                ('FLASH_TEST_STATUS', '1'),
                ('VM_MODULE_TEST_STATUS', '1'),
                ('Module_ID', 'VM501'),
                ('HW_version', 'HW:1.10'),
                ('software_version', 'SF:3.33_1900604'),
                ('address', 'ADDR:001'),
                ('type', 'IICA:A0H(160),'),
                ('serial_number', 'SN=576D57322036317E'),
                ],
    "beam_rl": [('BATTERY_TEST_STATUS', '1'),
                ('Battery_value', '3.593000'),
                ('Battery_unit', 'V'),
                ('BME_TEST_STATUS', '1'),
                ('BME_ID', '0x60'),
                ('TEMP', '26.559999'),
                ('TEMP_unit', 'C'),
                ('PRESSURE', '100875.804688'),
                ('PRESSURE_unit', 'Pa'),
                ('HUMIDITY', '36.254002'),
                ('HUMIDITY_unit', '%'),
                ('external_flash_status', '0'),
                ]
}

""" Sensor Diagnosis """
sensor_diagnosis = {
    "beam_vw": ["1600.0000 Hz 3000.0000 Ohm 99.9900 % 1234 ms"],
    "beam_an": ["0.1280 V 12.4999 V -1714.2857 ohm 2106 ms", "24.9999 mA -1714.2857 ohm 1766 ms"],
    "beam_tm": ["0.1280 V 12.4999 V -1714.2857 ohm 2106 ms"]
}
