import time
import random
import Params
from Params import SensorVariant
import Log
from Payload import GetFlashData


class CmdHandler:
    def __init__(self, configured_sensors, ser, func_serialWriteLogAndPrint):
        self.configured_sensors = configured_sensors
        self.ser = ser
        self.serial_write_log_and_print = func_serialWriteLogAndPrint

    def CheckAndHandleData(self, out):
        Log.LogAndPrint("<-- : " + out)
        out = out.strip()
        if (len(out)):
            self.__HandleData(out)
        else:
            reply = "Invalid Command\r\n"
            Log.LogAndPrint("--> : " + reply)

    def __HandleData(self, out):
        reply = "Received cmd : " + out + "\r\n"
        self.serial_write_log_and_print(reply)
        # Normal Commissioning flow
        if ("device_info" in out):
            self.__HandleDeviceInfo(out)
        elif ("channel_info" in out):
            self.__HandleChannelInfo(out, self.configured_sensors)
        elif ("channel_enable" in out):
            self.__HandleChannelEnable(out)
        elif ("start_monitoring" in out):
            self.__HandleStartMonitoring(out)
        elif ("read_sensor" in out):
            self.__HandleReadSensor(out, self.configured_sensors)
        elif ("get_address" in out):
            self.__HandleGetAddress(out)
        elif ("start_rfscan" in out):
            self.__HandleStartRFScan(out, self.ser)
        elif ("read_flash" in out):
            self.__HandleReadFlash(out)
        elif ("calibrate_sensor" in out):
            self.__HandleCalibrateSensor(out)
        elif ("erase_flash" in out):
            self.__HandleEraseFlash(out)
        elif ("util_diag" in out):
            self.__HandleUtilDiag(out)
        elif ("send_beacon" in out):
            self.__HandleSendBeacon(out)
        elif ("set_idle_mode" in out):
            self.__HandleSetIdleMode(out)
        elif ("sensor_diag" in out):
            self.__HandleSensorDiag(out)
        elif ("node_config" in out):
            self.__HandleNodeConfig(out)
        elif ("help" in out):
            print("Please use one of the commands below\n\tdevice_info\n\tchannel_info\n\tchannel_enable\n"
                  "\tstart_monitoring\n\tread_sensor\n\tget_address\n\tstart_rfscan\n\tread_flash\n\tcalibrate_sensor"
                  "\n\terase_flash\n\tutil_diag\n\tsend_beacon\n\tset_idle_mode\n\tsensor_diag\n\tnode_config")
        else:
            reply = "Command not found. Type 'help' for a list of commands\r\n"
            self.serial_write_log_and_print(reply)

    def __HandleDeviceInfo(self, out):
        """For the command device_info"""
        data = out.split()
        if len(data) > 1:
            # There is a chance that any of these params might be missing for some reason. If that's the case
            # just leave it as defaults specified in Params.py
            # For purposes of node simulator we just put placeholder information since this node doesn't transmit.
            try:
                Params.FREQUENCY = data[1]
                Params.SECRET_KEY = data[2]
                Params.TIME = data[3]
                Params.TX_POWER = data[4]
                Params.F_MIN = data[5]
                Params.F_MAX = data[6]
            except IndexError:
                Log.LogAndPrint("Device Info missing data. Filling in with placeholders...")
                # Leave Freq as the default in Params.
                # Leave Secret Key as the default in Params.
                # Leave time as the default in Params.
                Params.TX_POWER = "27"
                Params.F_MIN = "920000"
                Params.F_MAX = "925000"

        strDeviceId = str(Params.DEVICE_ID)
        strDeviceType = str(Params.DEVICE_TYPE)
        strMaxSensors = str(Params.MAX_SENSORS)
        strBattery = str(Params.BATTERY)
        strFrequency = str(Params.FREQUENCY)
        strIPI = str(Params.IPI)
        strSecretKey = str(Params.SECRET_KEY)
        strTime = str(Params.TIME)
        strRelayStatus = str(Params.RELAY_STATUS)
        strVersion = str(Params.VERSION)
        strTxPower = str(Params.TX_POWER)
        strFMin = str(Params.F_MIN)
        strFMax = str(Params.F_MAX)
        strSensorType = str(Params.SENSOR_TYPE.value)
        reply = "device_info " + strDeviceId + " " + strDeviceType + '_c' + \
                strMaxSensors + " " + strBattery + " " + strFrequency + " " + \
                strIPI + " " + strSecretKey + " " + strTime + " " + strRelayStatus + " " + \
                strVersion + " " + strTxPower + " " + strFMin + " " + strFMax + " " + \
                strSensorType + "\r\n"
        self.serial_write_log_and_print(reply)

    def __HandleChannelInfo(self, out, configured_sensors):
        """For the command channel_info"""
        reply = out + "\r\n"
        data = out.split(" ")
        configured_sensors[int(data[1])] = data[2:]
        self.serial_write_log_and_print(reply)

    def __HandleChannelEnable(self, out):
        """For the command channel_enable"""
        reply = out + "\r\n"
        self.serial_write_log_and_print(reply)

    def __HandleStartMonitoring(self, out):
        """For the command start_monitoring"""
        reply = out + "\r\n"
        data = out.split()
        Params.IPI = data[1]
        self.serial_write_log_and_print(reply)

    def __HandleReadSensor(self, out, configured_sensors):
        """For the command read_sensor"""
        time.sleep(random.randint(1, 5))
        data = out.split()

        """ Measurand """
        if (Params.SENSOR_TYPE == SensorVariant.MEASURAND):
            # TODO: Change this to read_sensor extended
            reply = "read_sensor 0 0 NA " + str(round(random.randint(0, 100) * 0.52435, 2)) + " V " + str(
                round(random.randint(0, 100) * 0.52435, 2)) + " mA " + str(
                round(random.randint(0, 100) * 0.52435, 2)) + " raw 101 ms\r\n"
            self.serial_write_log_and_print(reply)
            time.sleep(0.01)
            for i in range(1, int(data[1])):
                reply = "read_sensor " + str(i) + " " + str(round(random.randint(0, 65535), 0)) + " raw " + str(
                    round(random.randint(0, 65535), 0)) + " raw " + str(
                    round(random.randint(0, 65535), 0)) + " raw " + str(
                    round(random.randint(0, 65535), 0)) + " raw 0 ms\r\n"
                self.serial_write_log_and_print(reply)
                time.sleep(0.01)

        elif (Params.SENSOR_TYPE == SensorVariant.YIELDPOINT or Params.SENSOR_TYPE == SensorVariant.ESSEARTH_YP):
            """ Yieldpoint """
            # TODO: Change this to read_sensor extended
            units = ["mm", "C", "mm", "t", "degree"]
            reply = "read_sensor " + data[1]
            no_of_channels = 0
            if (len(Params.SENSOR_ADDRESS) == 10):
                no_of_channels = int(Params.SENSOR_ADDRESS[4:6])
            elif (len(Params.SENSOR_ADDRESS) == 9):
                no_of_channels = int(Params.SENSOR_ADDRESS[4])
            for i in range(no_of_channels):
                reply += " " + str(round(random.randint(0, 10000) * 0.52435, 4)) + " " + units[
                    random.randint(0, len(units) - 1)]
            reply += " " + str(random.randint(0, 10000)) + " ms\r\n"
            self.serial_write_log_and_print(reply)

        elif (Params.SENSOR_TYPE == SensorVariant.YIELDPOINT_DMUX):
            """ Yieldpoint dMux """
            # TODO: Change this to read_sensor extended
            units = ["mm", "C", "mm", "t", "degree"]
            reply = "read_sensor " + data[1]
            no_of_channels = 0
            if (len(Params.SENSOR_ADDRESS[int(data[1])]) == 10):
                no_of_channels = int(Params.SENSOR_ADDRESS[int(data[1])][4:6])
            elif (len(Params.SENSOR_ADDRESS[int(data[1])]) == 9):
                no_of_channels = int(Params.SENSOR_ADDRESS[int(data[1])][4])
            for i in range(no_of_channels):
                reply += " " + str(round(random.randint(0, 10000) * 0.52435, 4)) + " " + units[
                    random.randint(0, len(units) - 1)]
            reply += " " + str(random.randint(0, 10000)) + " ms\r\n"
            self.serial_write_log_and_print(reply)

        else:
            """ read_sensor and Extended read_sensor """
            sensors = []
            if (len(data) <= 2):
                sensors.append(int(data[1]))
            else:
                for id in range(1, len(data), 2):
                    sensors += list(range(int(data[id]), int(data[id + 1]) + 1))
            if (Params.SENSOR_TYPE == SensorVariant.SOIL_INSTRUMENTS):
                time.sleep(random.randint(4, 6))
            for sensor_id in sensors:
                time.sleep(random.randint(1, 20) * 0.1)
                sensor_id = str(sensor_id)
                if (Params.SENSOR_TYPE == SensorVariant.SDI12_GENERIC or \
                        Params.SENSOR_TYPE == SensorVariant.MDT_SMART_LINK or \
                        Params.SENSOR_TYPE == SensorVariant.SISGEO_DIGITAL):
                    """ MDT SMART LINK & SDI12 Generic & SISGEO"""
                    reply = "read_sensor " + sensor_id
                    for i in range(Params.NUM_OF_SENSOR_CHANNEL):
                        reply += " " + str(round(random.randint(0, 10000) * 0.52435, 4)) + " NA"
                    reply += " " + str(random.randint(0, 10000)) + " ms\r\n"

                elif (Params.SENSOR_TYPE == SensorVariant.SOIL_INSTRUMENTS):
                    """ SOIL INSTRUMENT"""
                    reply = "read_sensor " + sensor_id
                    for i in range(Params.NUM_OF_SENSOR_CHANNEL):
                        reply += " " + str(round(random.randint(0, 10000) * 0.52435, 4)) + " Deg"
                    reply += " " + str(random.randint(0, 10000)) + " ms\r\n"
                    if Params.SIMULATE_DELAY:
                        time.sleep(30)  # On avg it's 26-36s

                elif (Params.SENSOR_TYPE == SensorVariant.DATATAKER):
                    """ DATATAKER """
                    reply = "read_sensor " + sensor_id
                    for i in range(3):
                        reply += " " + str(round(random.randint(0, 10000) * 0.52435, 4)) + " NA"
                    reply += " " + str(random.randint(0, 10000)) + " ms\r\n"

                elif (Params.SENSOR_TYPE == SensorVariant.INSITU_AQUA_TROLL):
                    """ INSITU AQUA TROLL """
                    reply = "read_sensor " + sensor_id
                    reply += " " + str(round(random.randint(0, 10000) * 0.52435, 4)) + " NA"
                    reply += " " + str(random.randint(0, 10000)) + " ms\r\n"
                elif (
                        'beam_vw' in Params.DEVICE_TYPE or 'beam_an' in Params.DEVICE_TYPE or 'beam_tm' in Params.DEVICE_TYPE):
                    bit_vector = int(configured_sensors[int(sensor_id)][1])
                    bit_count = self.__countSetBits(bit_vector)
                    if bit_count == 3:
                        reply = "read_sensor " + sensor_id + " 1234.00 unit 78230.00 unit 21321.00 unit 101 ms\r\n"
                    elif bit_count == 2:
                        reply = "read_sensor " + sensor_id + " 1234.00 unit 78230.00 unit 101 ms\r\n"
                    elif bit_count == 1:
                        reply = "read_sensor " + sensor_id + " 78230.00 unit 101 ms\r\n"
                    else:
                        reply = "read_sensor " + sensor_id + " 101 ms\r\n"
                    time.sleep(1)
                elif (Params.SENSOR_TYPE == SensorVariant.GEOSENSE_IPTM):  # 9
                    reply = "read_sensor " + sensor_id + " -0.0030 NA -0.0012 NA 23.8999 C 3289 ms\r\n"
                    time.sleep(1)
                else:
                    """ All other sensors """
                    time.sleep(1)
                    reply = "read_sensor " + sensor_id + " 1234.00 unit 78230.00 unit 21321.00 unit 101 ms\r\n"
                self.serial_write_log_and_print(reply)

    def __countSetBits(self, n):
        count = 0
        while (n):
            count += n & 1
            n >>= 1
        return count

    def __HandleGetAddress(self, out):
        """For the command get_address"""
        reply = ""
        if Params.SENSOR_TYPE == SensorVariant.MEASURAND:
            data = out.split()  # e.g. ['get_address', '22', '200']
            sensors = int(data[2]) + 1  # +1 cause sensor type 22 always has 1x sensor 26.
            reply = "get_address " + data[1] + " " + str(sensors) + " 350208"
            for i in range(sensors - 1):
                reply += " " + str(350208 + i)
            reply += "\r\n"
        elif Params.SENSOR_TYPE == SensorVariant.YIELDPOINT:
            data = out.split()
            reply = "get_address " + str(data[1]) + " 1 " + str(Params.SENSOR_ADDRESS[0]) + "\r\n"
        elif Params.SENSOR_TYPE == SensorVariant.YIELDPOINT_DMUX or Params.SENSOR_TYPE == SensorVariant.SOIL_INSTRUMENTS or Params.SENSOR_TYPE == SensorVariant.ESSEARTH_HIDCELL or Params.SENSOR_TYPE == SensorVariant.ESSEARTH_YP:
            data = out.split()
            if Params.SENSOR_ADDRESS == 0 and Params.SENSOR_TYPE == SensorVariant.SOIL_INSTRUMENTS:
                Params.SENSOR_ADDRESS = ["3450-0", "3451-1", "3452-2", "3453-3", "3454-4"]
            elif Params.SENSOR_ADDRESS == 0 and Params.SENSOR_TYPE == SensorVariant.YIELDPOINT_DMUX:
                Params.SENSOR_ADDRESS = ["0", "0", "0", "210194721"]
            reply = "get_address " + data[1] + " " + str(len(Params.SENSOR_ADDRESS))
            for adr in Params.SENSOR_ADDRESS:
                reply += " " + adr
            reply += "\r\n"
            time.sleep(2)
        elif Params.SENSOR_TYPE == SensorVariant.MDT_SMART_LINK:
            data = out.split()
            reply = "get_address " + data[1] + " 1"
            reply += " " + str(Params.SENSOR_ADDRESS[0])
            reply += "\r\n"
        elif Params.SENSOR_TYPE == SensorVariant.DATATAKER or Params.SENSOR_TYPE == SensorVariant.INSITU_AQUA_TROLL:
            data = out.split()
            reply = "get_address " + data[1] + " " + str(Params.MAX_SENSORS)
            for i in range(int(Params.MAX_SENSORS)):
                reply += " " + str(Params.SENSOR_ADDRESS[i]) + "-" + str(i)
            reply += "\r\n"

        if Params.SIMULATE_FAILURE_GET_ADDRESS:
            Log.LogAndPrint("Simulate failure to get_address with a no reply.")
        else:
            self.serial_write_log_and_print(reply)

    def __HandleStartRFScan(self, out, ser):
        """For the command start_rfscan"""
        Params.NUM_OF_CHANNEL = (int(Params.F_MAX) - int(Params.F_MIN)) / 200
        if Params.NUM_OF_CHANNEL > 120: Params.NUM_OF_CHANNEL = 120
        reply = "start_rfscan "
        for i in range(int(Params.NUM_OF_CHANNEL)):
            reply += str(((int(Params.F_MIN) + 100) + (i * 200))) + " "
        reply += "\r\n"
        self.serial_write_log_and_print(reply)
        while True:
            out = ser.readline().decode('utf-8')
            if "stop_rfscan" in out:
                reply = out
                self.serial_write_log_and_print(reply)
                break
            self.__GenerateNoiseData()
            time.sleep(1)

    def __GenerateNoiseData(self):
        reply = "rf_noise "
        for i in range(int(Params.NUM_OF_CHANNEL)):
            n = random.randint(70, 120)
            reply += "-" + str(n) + " "
        reply += "\r\n"
        self.serial_write_log_and_print(reply)

    def __HandleReadFlash(self, out):
        """For the command read_flash"""
        data = out.split()
        flashData = GetFlashData(int(Params.DEVICE_ID, 16), int(data[1]), int(Params.IPI), Params.SENSOR_TYPE)
        self.__PrintFlash(flashData)

    def __PrintFlash(self, rawFlash):
        for s in range(1, len(rawFlash) + 1):
            reply = "Flash " + rawFlash[-s] + "\r\n"
            self.serial_write_log_and_print(reply)
        reply = "flash_read " + str(len(rawFlash)) + "\r\n"
        self.serial_write_log_and_print(reply)

    def __HandleCalibrateSensor(self, out):
        """For the command calibrate_sensor"""
        data = out.split()
        reply = ""
        if (len(data) > 1):
            REPLY_1 = out + "\r\n"
            # Replace data[2] - data [5] with "ERROR"
            # eg : data[0] + data[1] + data[2] + "ERROR" + data[4] + data[5] + "\r\n"
            REPLY_2 = data[0] + " " + data[1] + " " + data[2] + " " + "ERROR" + " " + data[4] + " " + data[5] + " " + \
                      data[6] + "\r\n"
            # For correct output use REPLY_1, for error value use REPLY_2
            reply = REPLY_1
            Params.CALIBRATION[int(data[1])] = out.split("sensor " + data[1] + " ")[1]
        else:
            reply += "calibrate_sensor 0 " + str(Params.CALIBRATION[0]) + "\r\n"
            reply += "calibrate_sensor 1 " + str(Params.CALIBRATION[1]) + "\r\n"
        self.serial_write_log_and_print(reply)

    def __HandleEraseFlash(self, out):
        """For the command erase_flash"""
        reply = out + " 1\r\n"
        self.serial_write_log_and_print(reply)

    def __HandleUtilDiag(self, out):
        """For the command util_diag"""
        reply = "util_diag"
        for util_params in Params.util_diagnosis[Params.DEVICE_TYPE]:
            reply += " " + util_params[1]
        reply += "\r\n"
        self.serial_write_log_and_print(reply)

    def __HandleSendBeacon(self, out):
        """For the command send_beacon"""
        reply = out + "\r\n"
        self.serial_write_log_and_print(reply)

    def __HandleSetIdleMode(self, out):
        """For the command set_idle_mode"""
        reply = out + "\r\n"
        self.serial_write_log_and_print(reply)

    def __HandleSensorDiag(self, out):
        """For the command sensor_diag"""
        reply = "sensor_diag " + str(
            int(Params.MAX_SENSORS) * len(Params.sensor_diagnosis[Params.DEVICE_TYPE])) + "\r\n"
        self.serial_write_log_and_print(reply)
        time.sleep(random.randint(1, 5))
        for sensor_id in range(int(Params.MAX_SENSORS)):
            for diagnosis in Params.sensor_diagnosis[Params.DEVICE_TYPE]:
                reply = "read_sensor " + str(sensor_id) + " " + diagnosis + "\r\n"
                self.serial_write_log_and_print(reply)
                time.sleep(random.randint(1, 5))

    def __HandleNodeConfig(self, out):
        """For the command node_config"""
        data = out.strip().split(" ")
        if (data[1] == "1"):
            """ Network Size """
            if (len(data) == 3):
                Params.NETWORK_SIZE = data[2]
            reply = "node_config " + data[1] + " " + str(Params.NETWORK_SIZE) + " " + str(Params.MIN_SAMPLING_INTERVAL)
        elif (data[1] == "2"):
            """ Flash Retransmission """
            if (len(data) == 3):
                Params.FLASH_RETRANSMISSION = data[2]
            reply = "node_config " + data[1] + " " + str(Params.FLASH_RETRANSMISSION)
        else:
            reply = "node_config -1"
        reply += "\r\n"

        self.serial_write_log_and_print(reply)
