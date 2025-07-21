from .Custom_TestCase import Custom_TestCase
from .BeamAN_VW1_TestCase import BeamAN_VW1_TestCase
from .BeamAN_VW1_Network_TestCase import BeamAN_VW1_Network_TestCase
from .NetworkTest_Range_TestCase import NetworkTest_Range_TestCase
from .NetworkTest_UIBurst_TestCase import NetworkTest_UIBurst_TestCase
from .NetworkTest_Continuous_TestCase import NetworkTest_Continuous_TestCase
from .BeamDG_GeoSense_TestCase import BeamDG_GeoSense_TestCase
from .Measurand_TestCase import Measurand_TestCase
from .SoilInstrument_WithDelay_TestCase import SoilInstrument_WithDelay_TestCase
from .YieldPointDMUX_WithFailure_TestCase import YieldPointDMUX_WithFailure_TestCase
from .BeamRN_TestCase import BeamRN_TestCase
from .Saved_TestCase import Load_Saved_TestCase, Save_New_TestCase, Delete_TestCase


def generate_test_cases(serialSim):
    testCases = [
        Custom_TestCase("CUSTOM", serialSim),
        Load_Saved_TestCase("Load from SAVED Test Cases", serialSim),
        Save_New_TestCase("ADD a NEW Test Case to memory", serialSim),
        Delete_TestCase("Delete a saved Test Case", serialSim),
        BeamAN_VW1_TestCase("BEAM-AN VW1", serialSim),
        BeamAN_VW1_Network_TestCase("BEAM-AN VW1 with Network Test", serialSim),
        NetworkTest_Range_TestCase("Network Test Range", serialSim),
        NetworkTest_UIBurst_TestCase("Network Test UI Burst", serialSim),
        NetworkTest_Continuous_TestCase("Network Test Continuous", serialSim),
        BeamDG_GeoSense_TestCase("BEAM-DG GeoSense", serialSim),
        Measurand_TestCase("Measurand", serialSim),
        SoilInstrument_WithDelay_TestCase("Soil Instrument with Delay", serialSim),
        YieldPointDMUX_WithFailure_TestCase("YieldPointDMUX with Failure", serialSim),
        BeamRN_TestCase("BEAM-RN", serialSim)
    ]

    return testCases
