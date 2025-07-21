import struct
import json


def GetSizeOf(type):
    if (type <= 3):
        return 4
    elif (type <= 5):
        return 2
    else:
        return 1


def HexStringToIntList(sample):
    return [int(sample[i:i + 2], 16) for i in range(0, len(sample), 2)]


def Parser(dataArray):
    dataPointer = 0
    srcAddress = struct.unpack('>H', bytearray(dataArray[dataPointer:dataPointer + 2]))[0]
    dataPointer += 2
    packetSize = struct.unpack('<B', bytearray(dataArray[dataPointer:dataPointer + 1]))[0]
    dataPointer += 1
    timeStamp = struct.unpack('<I', bytearray(dataArray[dataPointer:dataPointer + 4]))[0]
    dataPointer += 4
    SensorType = struct.unpack('<B', bytearray(dataArray[dataPointer:dataPointer + 1]))[0]
    dataPointer += 1
    dataType = SensorType & 0xF
    noOfData = (SensorType >> 4) & 0xF

    dataSize = GetSizeOf(dataType)
    noOfSensors = (packetSize - 6) / (1 + noOfData * dataSize)
    sensorData = []
    for i in range(int(noOfSensors)):
        sensorId = struct.unpack('<B', bytearray(dataArray[dataPointer:dataPointer + 1]))[0]
        dataPointer += 1
        data = {}
        for j in range(noOfData):
            if (dataType == 1):  # float
                tempData = struct.unpack('f', bytearray(dataArray[dataPointer:dataPointer + dataSize]))[0]
            elif (dataType == 2):  # Int32
                tempData = struct.unpack('i', bytearray(dataArray[dataPointer:dataPointer + dataSize]))[0]
            elif (dataType == 3):  # UInt32
                tempData = struct.unpack('I', bytearray(dataArray[dataPointer:dataPointer + dataSize]))[0]
            elif (dataType == 4):  # Int16
                tempData = struct.unpack('h', bytearray(dataArray[dataPointer:dataPointer + dataSize]))[0]
            elif (dataType == 5):  # UInt16
                tempData = struct.unpack('H', bytearray(dataArray[dataPointer:dataPointer + dataSize]))[0]
            elif (dataType == 6):  # Int8
                tempData = struct.unpack('b', bytearray(dataArray[dataPointer:dataPointer + dataSize]))[0]
            elif (dataType == 7):  # UInt8
                tempData = struct.unpack('B', bytearray(dataArray[dataPointer:dataPointer + dataSize]))[0]
            dataPointer += dataSize
            data[str(j)] = float(tempData)
        sensorData.append({"sensorId": sensorId, "values": data})

    # JSON
    result = {}
    result["srcAddress"] = str(hex(srcAddress))[2:]
    result["timeStamp"] = timeStamp
    result["sensorData"] = sensorData
    json_result = json.dumps(result, sort_keys=True)
    return json_result
