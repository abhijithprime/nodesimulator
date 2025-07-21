import struct
import time
import binascii
from enum import Enum

MAX_DATA_PER_SENSOR = 8
MAX_DATATYPE_SUPPORT = 7
MAX_MTU_SIZE = 75
MAX_ALLOWED_SENSORS = 256

FlashFile = [[0] * 32 for _ in range(MAX_ALLOWED_SENSORS)]
rawFlash = []
dataInfo = [0] * MAX_ALLOWED_SENSORS
CurrentTime = 0
packetTime = 0
nodeID = 0x1234

class SensorVariant(Enum):
    MEASURAND = 1
    OTHER = 2

def getClockStartTime(sampleInt):
    mod = CurrentTime % (sampleInt * 60)
    return (sampleInt * 60 - mod)

def GetSizeOf(type):
    if type <= 3:
        return 4
    elif type <= 5:
        return 2
    else:
        return 1

def PutToDataBuffer(sensorId, noOfData, dataType, data):
    block_write(0, sensorId, data)
    dataInfo[sensorId] = noOfData << 4 | dataType

def block_write(file, ptr, data):
    FlashFile[ptr] = data

def block_read(file, ptr, data):
    return FlashFile[ptr]

def generatePayload():
    noOfData = 0
    dataType = 0
    sensorId = 0
    data = [0] * 32
    payloadBuffer = [0] * 128

    dataPointer = 0
    payloadBuffer[dataPointer] = 0
    dataPointer += 1
    packetTimeRaw = struct.pack('<I', packetTime)
    payloadBuffer[dataPointer:dataPointer + 4] = list(packetTimeRaw)
    dataPointer += 4

    for noOfData in range(1, MAX_DATA_PER_SENSOR):
        for dataType in range(1, MAX_DATATYPE_SUPPORT):
            sensorType = noOfData << 4 | dataType
            payloadBuffer[dataPointer] = sensorType
            dataPointer += 1

            for sensorId in range(0, MAX_ALLOWED_SENSORS):
                if dataInfo[sensorId] == sensorType:
                    data = block_read(0, sensorId, data)
                    sizeOfData = noOfData * GetSizeOf(dataType)

                    if dataPointer + sizeOfData < MAX_MTU_SIZE:
                        payloadBuffer[dataPointer] = sensorId
                        dataPointer += 1
                        payloadBuffer[dataPointer:dataPointer + sizeOfData] = data[:sizeOfData]
                        dataPointer += sizeOfData
                    else:
                        srcAddress = nodeID
                        srcAddressRaw = struct.pack('>H', srcAddress)
                        sendBuffer = list(srcAddressRaw) + payloadBuffer[:dataPointer]
                        sendBuffer[2] = dataPointer
                        rawFlash.append(binascii.hexlify(bytearray(sendBuffer)).decode())
                        dataPointer = 6
                        payloadBuffer[dataPointer:] = [0] * (MAX_MTU_SIZE - dataPointer)
                        payloadBuffer[dataPointer] = sensorId
                        dataPointer += 1
                        payloadBuffer[dataPointer:dataPointer + sizeOfData] = data[:sizeOfData]
                        dataPointer += sizeOfData

            if dataPointer > 6:
                srcAddress = nodeID
                srcAddressRaw = struct.pack('>H', srcAddress)
                sendBuffer = list(srcAddressRaw) + payloadBuffer[:dataPointer]
                sendBuffer[2] = dataPointer
                rawFlash.append(binascii.hexlify(bytearray(sendBuffer)).decode())

            dataPointer = 5
            payloadBuffer[dataPointer:] = [0] * (MAX_MTU_SIZE - dataPointer)

def PrintFlash():
    for s in range(1, len(rawFlash) + 1):
        print("Flash", rawFlash[-s], "\r\n")

def AddAData(sensorId, noOfData, dataType):
    dataSize = GetSizeOf(dataType)
    data = [0] * 32
    for i in range(noOfData):
        if dataType == 1:
            sampleData = 1234.9876
            data[i * dataSize:(i + 1) * dataSize] = list(struct.pack('f', sampleData))
        elif dataType == 2:
            sampleData = 12349876
            data[i * dataSize:(i + 1) * dataSize] = list(struct.pack('i', sampleData))
        elif dataType == 3:
            sampleData = 12349876
            data[i * dataSize:(i + 1) * dataSize] = list(struct.pack('I', sampleData))
        elif dataType == 4:
            sampleData = 47882
            data[i * dataSize:(i + 1) * dataSize] = list(struct.pack('h', sampleData))
        elif dataType == 5:
            sampleData = 4882
            data[i * dataSize:(i + 1) * dataSize] = list(struct.pack('H', sampleData))
        elif dataType == 6:
            sampleData = 254
            data[i * dataSize:(i + 1) * dataSize] = list(struct.pack('b', sampleData))
        elif dataType == 7:
            sampleData = 123
            data[i * dataSize:(i + 1) * dataSize] = list(struct.pack('B', sampleData))
    PutToDataBuffer(sensorId, noOfData, dataType, data)

def GetFlashData(id, day, IPI, sensorType, num_records=40000):  # Added num_records parameter
    global nodeID, packetTime, CurrentTime, rawFlash
    rawFlash = []
    CurrentTime = int(time.time())
    nodeID = id
    NextIPI = getClockStartTime(IPI)
    
    records_generated = 0
    start_time = CurrentTime + NextIPI - day * 60 * 3600
    
    while records_generated < num_records:
        for t in range(start_time, CurrentTime + NextIPI, IPI * 60):
            packetTime = t
            if sensorType == SensorVariant.MEASURAND:
                AddAData(0, 4, 1)
                NOOFSENSORS = 100
                DATATYPE = 5
                NOOFDATAPERSENSOR = 4
                for i in range(1, NOOFSENSORS + 1):
                    AddAData(i, NOOFDATAPERSENSOR, DATATYPE)
            else:
                NOOFSENSORS = 8
                DATATYPE = 1
                NOOFDATAPERSENSOR = 3
                for i in range(NOOFSENSORS):
                    AddAData(i, NOOFDATAPERSENSOR, DATATYPE)
            generatePayload()
            records_generated += len(rawFlash) - records_generated #Increment by the amount of records generated in this payload
            if records_generated >= num_records:
                break
        start_time += IPI * 60  # Move the start time forward

    return rawFlash[:num_records] # return only the amount of records requested.