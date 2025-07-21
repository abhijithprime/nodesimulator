import Params
from Params import SensorVariant
import sys
import glob
import serial
import threading
import SerialSim
import TestCases.TestCaseGenerator as TestCaseGenerator
import Log
import JsonHandler
from TestCases.Saved_TestCase import Load_Saved_TestCase


###############
# NORMAL MODE #
###############

def get_list_serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


def prompt_user_for_port():
    detectedPorts = []

    # Select the PORT
    selectedPortIndex: int = -1
    while selectedPortIndex < 0:
        detectedPorts = get_list_serial_ports()
        print("Listing available ports...")
        for i in range(len(detectedPorts)):
            print("\t", str(i) + ".", detectedPorts[i])

        inputStr: str = input("Select Port to test on (just enter to refresh): ")
        try:
            inputInt = int(inputStr)
            if inputInt < len(detectedPorts) and inputInt >= 0:
                selectedPortIndex = inputInt
        except ValueError:
            pass
    Params.PORT = detectedPorts[selectedPortIndex]
    print("Selected Port: [" + str(selectedPortIndex) + "]", Params.PORT)


def prompt_user_for_test_type():
    node_history_list_of_dictionaries = []
    node_history_list_of_dictionaries = JsonHandler.load_from_json()
    serialSim = SerialSim.SerialSim()
    testCases = TestCaseGenerator.generate_test_cases(serialSim)

    selectedTestCase: int = -1

    breakpoint_index_between_primary_and_secondary_testcases = 4  # This simply seperates the primary and secondary testcases in the testcases list
    # select a test case as an integer among the given values
    while selectedTestCase < 0:
        print("\nPrimary Test Cases")
        for i in range(breakpoint_index_between_primary_and_secondary_testcases):
            print("\t", str(i) + ".", testCases[i].getTestName())
        print("\nSecondary Test Cases")
        for i in range(breakpoint_index_between_primary_and_secondary_testcases, len(testCases)):
            print("\t", str(i) + ".", testCases[i].getTestName())

        inputStr: str = input("Please select test type: ")
        try:
            inputInt = int(inputStr)
            if inputInt < len(testCases) and inputInt >= 0:
                selectedTestCase = inputInt
        except ValueError:
            pass
    testCase = testCases[selectedTestCase]
    Log.LogAndPrint("Running selected test case: [{}] {}".format(selectedTestCase, testCase.getTestName()))
    Params.resetSimulateParams()
    testCase.set_params()
    serialSim.update_configured_sensors_array()

    try:
        testCase.run_test()
    except KeyboardInterrupt:
        Log.LogEndOfSession()


def run_normal_mode():
    try:
        prompt_user_for_port()
        prompt_user_for_test_type()
    except KeyboardInterrupt:
        Log.LogEndOfSession()


####################
# PARAMETER MODE #
####################

def run_param_mode():
    """Run a saved node by giving port and device ID as parameters. Example: python Tester.py -p COM9 -d ad04"""
    given_arguments = sys.argv

    # Getting the port
    if "-p" in given_arguments:
        try:
            port = str(given_arguments[given_arguments.index("-p") + 1])
            print("Trying to load port", port)
        except IndexError:
            print(
                "Invalid Arguments. Please follow the Syntax below.\npython Tester.py -p {_port name_} -d {_device ID_}")
            return
    else:
        print("Please provide a valid port using -p argument and rerun the program")
        return

    Params.PORT = port
    try:
        serialSim = SerialSim.SerialSim()
    except serial.serialutil.SerialException:
        print("Port number is not valid. Use one of the available ports shown below.")
        detectedPorts = get_list_serial_ports()
        print(' '.join(detectedPorts))
        return

    # Getting the device ID
    if "-d" in given_arguments:
        try:
            device_id = str(given_arguments[given_arguments.index("-d") + 1])
            print("Loading device ID", device_id)
        except IndexError:
            print(
                "Invalid Arguments. Please follow the Syntax below.\npython Tester.py -p {_port name_} -d {_device ID_}")
            return
    else:
        print("Please provide a 4 character device ID using -d argument and rerun the program")
        return

    testCase = Load_Saved_TestCase("Load from SAVED Test Cases", serialSim)
    Log.LogAndPrint("Running selected test case: {}".format(testCase.getTestName()))
    Params.resetSimulateParams()
    status = testCase.set_arg_params(device_id)
    if status != 0:
        Log.LogAndPrint("Parameter mode failed at setting parameters")
        return
    serialSim.update_configured_sensors_array()
    try:
        testCase.run_test()
    except KeyboardInterrupt:
        Log.LogEndOfSession()


def main():
    print("WELCOME TO PYTHON SERIAL TESTER FOR NIMBUS")
    if len(sys.argv) > 1:
        run_param_mode()
    else:
        run_normal_mode()


if __name__ == '__main__':
    main()
