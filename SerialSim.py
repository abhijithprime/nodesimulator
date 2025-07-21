import serial
import time
import datetime
from datetime import datetime
import random
import Params
import Log
from Payload import GetFlashData
import CmdHandler
from Params import SensorVariant


###############################
# BELOW HERE ARE OLD COMMENTS #
###############################
# BEAM AN,VW, TM & RN
# python3 SerialSim.py <port> <device_id> <device_type> <no_of_sensors> <sensor_type> <sensor_address>
# if sensortype is not require then will send 0
# python3 SerialSim.py /dev/ttyACM0 abcd beam_vw 8 0
# python3 SerialSim.py /dev/ttyACM0 abcd beam_vw 1 0
# python3 SerialSim.py /dev/ttyACM0 abcd beam_an 1 0
# python3 SerialSim.py /dev/ttyACM0 abcd beam_an 4 0
# BEAM TM
# SISGEO_TILT_METER       = 30
# ENCARDIO_TILT_METER     = 31
# GEOGAGE_TILT_METER      = 32
# python3 SerialSim.py /dev/ttyACM0 abcd beam_tm 1 30
# BEAM-DG : MEASURAND
# python3 SerialSim.py /dev/ttyACM0 abcd beam_dg 4 22
# BEAM-DG : YIELDPOINT
# python3 SerialSim.py /dev/ttyACM0 abcd beam_dg 32 27 181041012
# BEAM-DG : YIELDPOINT dMUX
# python3 SerialSim.py /dev/ttyACM0 6767 beam_dg 32 29 181052013 181071015 181023016 181056017
# BEAM-DG : SDI12 Generic
# python3 SerialSim.py /dev/ttyACM0 6767 beam_dg 32 34 3
# BEAM-DG : MDT
# python3 SerialSim.py /dev/ttyACM0 abcd beam_dg 32 35 181041012 8
# BEAM-DG : DATA_TAKER
# python3 SerialSim.py /dev/ttyACM0 abcd beam_dg 32 36 181041012
# BEAM-DG : INSITU_AQUA_TROLL
# python3 SerialSim.py /dev/ttyACM0 abcd beam_dg 10 37 1
# BEAM-DG : Sisgeo Digital
# python3 SerialSim.py /dev/ttyACM0 6767 beam_dg 32 39 9
# BEAM-DG : Soil instrument
# python3 SerialSim.py /dev/ttyACM0 6767 beam_dg 32 40 5 15429-0 15685-1


class SerialSim:
    def __init__(self):
        print("Sensor Type : ", Params.SENSOR_TYPE.value)
        self.ser = serial.Serial(Params.PORT, Params.BAUD, timeout=0)
        self.update_configured_sensors_array()
        if self.ser.isOpen():
            print(self.ser.name + ' is open...')

    def update_configured_sensors_array(self):
        numSensors: int = int(Params.MAX_SENSORS)
        if Params.SENSOR_TYPE == SensorVariant.MEASURAND:
            numSensors += 1  # For the 1x sensor id 26.
        self.configured_sensors = [None] * numSensors

    def serial_write_log_and_print(self, reply):
        if len(reply) > 0:
            self.ser.write(reply.encode('utf-8'))
            Log.LogAndPrint("--> : " + reply)

    def read_from_port(self, serP):
        cmdHandler = CmdHandler.CmdHandler(self.configured_sensors, self.ser, self.serial_write_log_and_print)
        print("\n\nSerial read Started")
        last_command_time = datetime.timestamp(datetime.now())
        time.sleep(0.2)
        while True:
            try:
                reading = serP.readline().decode('utf-8')

                if (len(reading)):
                    if ((datetime.timestamp(datetime.now()) - last_command_time) < 0.1):
                        reply = "Error : Command too fast\r\n"
                        Log.LogAndPrint("--> : " + reply)
                    else:
                        cmdHandler.CheckAndHandleData(reading)
                    last_command_time = datetime.timestamp(datetime.now())

                time.sleep(0.1)
            except UnicodeDecodeError as error:
                print("Error : UnicodeDecodeError")

    def nbr_info(self, serP):
        while True:
            reply = ""
            if (random.randint(0, 5)):
                rssi = -22
                nodeId = 0x5a52 + random.randint(0, 5)
                reply = "nbr_info " + str(hex(nodeId))[2:] + " node NA NA -" + str(random.randint(20, 90)) + "\r\n"
            else:
                reply = "[INFO: TSCH-LOG  ] {asn 00.0003de9f link  1  11   0  5 216 ch  9} uc-1-0 rx LL-57eb->LL-57d6, len  63, seq 117, edr   2, dr  -2\r\n"

            self.serial_write_log_and_print(reply)
            time.sleep(5)

    def handle_terminal_data(self, serial_port, data):
        if ("reboot" in data):
            reply = "DEVICE ID   : " + Params.DEVICE_ID + "\r\n"
            self.serial_write_log_and_print(reply)

    def read_from_terminal(self, serial_port):
        while (1):
            _terminal_input = input()
            # print("Received from terminal : ",terminal_input)
            self.handle_terminal_data(serial_port, _terminal_input)
