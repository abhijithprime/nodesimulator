import datetime
import os


class __Logger:
    def __init__(self):
        FOLDER_PATH = os.path.join(os.getcwd(), "logs")
        if not os.path.exists(FOLDER_PATH):
            os.makedirs(FOLDER_PATH)
        filename = "commonlog_" + str(datetime.datetime.now()) + ".log"
        self.__currentFileName = os.path.normpath(os.path.join(FOLDER_PATH, filename))

    def LogAndPrint(self, msg):
        print(str(datetime.datetime.now().strftime("%H:%M:%S.%f")) + " : " + msg)
        self.LogLine(msg)

    def LogLine(self, msg):
        self.__currentFileName = "logs\\commonlog.log"
        f = open(self.__currentFileName, "a")
        f.write(str(datetime.datetime.now()) + " : " + msg)
        f.close()


__currentLogger = __Logger()


def LogAndPrint(msg):
    __currentLogger.LogAndPrint(msg)


def LogEndOfSession():
    print("\n\n")
    __currentLogger.LogAndPrint("Node Simulation session ended by user.")
