# Python Seiral Testing Tool
Used for testing the Nimbus app. The python tool simulates what a Node would respond to serial commands from the Nimbus app.

In order to use it, make sure you have a UART cable and python 3.11 installed on your device.

<br />

## Normal Mode
To use the tool normally, simply cd to the repository folder in terminal (where `Tester.py` is located). Then type in the command `python3 Tester.py`. You will then see a list of available serial ports (this is the same result if you type in `ls /dev/tty.*`) for you to select. If you're having difficulty figuring out which is the one, then you can start the Tester tool first, then plug in the UART port to your computer, hit enter to refresh the tool and the new port that popped up is the one to use.

After selecting the port to run the tool on, you'll be presented with a list of Test Cases for you to run. Just enter the corresponding number for the desired Test Case.

There is a special Test Case called `Custom` which allows you to specify the exact Node parameters, from the Beam_AN/Beam_DG to the max sensors, and the sensor type. _<<<**THIS IS WORK IN PROGRESS!!! NEEDS MORE UNDERSTANDING OF SPECIAL NODE TAKES THAT HAVE WAY MORE PARAMETERS**>>>_

<br />

### Expanding/Writing New Test Cases
To write a new Test Case, simply create a new file under `TestCases/`. You may reference the other TestCases but generally you will need to import BaseTestCase using `from .BaseTestCase import BaseTestCase` and then define your New_TestCase class as a subclass of BaseTestCase `class New_TestCase(BaseTestCase):`.

In your TestCase class you will also need to implement two functions the:
- `def set_params(self)`
    - Function that sets the following
    - `Params.DEVICE_TYPE`
    - `Params.MAX_SENSORS`
    - `Params.SENSOR_TYPE`
- `def run_test(self)`
    - Function that runs the actual threads for the simulated Node Behaviour
    - `self.run_thread_read_from_port()`
    - `self.run_thread_nbr_info()`
    - `self.run_thread_read_from_terminal()`
    - Or a custom thread behaviour

After creating your TestCase class, you will need to add it into the `TestCases/TestCaseGenerator.py` under the `generate_test_cases` function. Simply add it into the `testCases` array as an instance. After that you should be able to run the Test tool normally and select your new Test Case to try it out.



<br />
<br />

## Arguments Mode

This method is for the automation of simulation.

In this mode, it takes in the com port and device ID as arguments and simulate the device indicated by the device ID in the device history.

Syntax : **python Tester.py -p {_port name_} -d {_device ID_}**
<br/>
e.g. `python3 Tester.py COM9 abcd`