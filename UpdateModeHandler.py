# Diff between received and sent bin file data : https://www.diffchecker.com/9bwr60WV/
# Diff between original bin file as decimal and send (received) data : https://www.diffchecker.com/yykfKOQR/


import Log
import time
import os
import binascii

# # Uncomment these for the actual Nimbus app in phone
waiting_time_before_receiving_data = 0.1
waiting_time_before_ack = 0.1
waiting_time_after_mem_reads_commands = 0.1
waiting_time_before_sending_response = 0.05

# # Uncomment these for the simulator burn.py in PC
# waiting_time_before_receiving_data = 0.03
# waiting_time_before_ack = 0
# waiting_time_after_mem_reads_commands = 0
# waiting_time_before_sending_response = 0

commands_ret_dict = {"COMMAND_RET_SUCCESS": bytearray([0x40]), "COMMAND_RET_UNKNOWN_CMD": 0x41,
                     "COMMAND_RET_INVALID_CMD": 0x42,
                     "COMMAND_RET_INVALID_ADR": 0x43, "COMMAND_RET_FLASH_FAIL": 0x44}

commands_incoming_dict = {0x23: "COMMAND_GET_STATUS", 0x25: "COMMAND_RESET", 0x28: "COMMAND_GET_CHIP_ID",
                          0x21: "COMMAND_DOWNLOAD", 0x24: "COMMAND_SEND_DATA", 0x27: "COMMAND_CRC32", 0x2A: "MEM_READ",
                          0x2C: "COMMAND_BANK_ERASE"}

command_vs_response = {"COMMAND_GET_STATUS": commands_ret_dict["COMMAND_RET_SUCCESS"],
                       "COMMAND_GET_CHIP_ID": bytearray([0xa2, 0x20, 0x02, 0x80])
                       }

mem_read_address_list = [bytearray([0x2a, 0x50, 0x00, 0x13, 0x18, 0x01, 0x01]),  # device ID
                         bytearray([0x2a, 0x50, 0x00, 0x12, 0x94, 0x01, 0x01]),  # user ID
                         bytearray([0x2a, 0x50, 0x00, 0x10, 0xa0, 0x01, 0x01]),  # chip name
                         bytearray([0x2a, 0x40, 0x03, 0x00, 0x2c, 0x01, 0x01]),  # flash size
                         bytearray([0x2a, 0x40, 0x08, 0x22, 0x50, 0x01, 0x01]),  # ram size
                         bytearray([0x2a, 0x50, 0x00, 0x12, 0xF4, 0x01, 0x01]),  # IEEE adr p 1 : 2A 50 00 12 F4 01 01
                         bytearray([0x2a, 0x50, 0x00, 0x12, 0xF0, 0x01, 0x01])  # IEEE adr p 2 : 2A 50 00 12 F0 01 01
                         ]

mem_read_data_list = [bytearray([0x2F, 0xE0, 0x9B, 0x2B]),  # device ID
                      bytearray([0x00, 0x80, 0x02, 0x20]),  # user ID
                      bytearray([0x01, 0xff, 0xff, 0xff]),  # chip name
                      bytearray([0x20, 0x00, 0x00, 0x00]),  # flash size
                      bytearray([0x03, 0x00, 0x00, 0x00]),  # ram size
                      bytearray([0x00, 0x4B, 0x12, 0x00]),  # IEEE adr p 1 : 00 4B 12 00
                      bytearray([0x6B, 0xD3, 0x8C, 0x22])  # IEEE adr p 2 : 6B D3 8C 22
                      ]


class CmdException(Exception):
    pass


class FirmwareFile(object):
    def __init__(self):
        self._crc32 = None
        self.bin_file = []

    def crc32(self, original_file_len):
        """
        Return the crc32 checksum of the firmware image

        Return:
            The firmware's CRC32, ready for comparison with the CRC
            returned by the ROM bootloader's COMMAND_CRC32
        """
        self._crc32 = None
        if self._crc32 is None:
            self._crc32 = binascii.crc32(bytearray(self.bin_file)) & 0xffffffff
        return self._crc32

    def fillEmptyPackets(self, original_full_length, remaining_length_of_data_to_receive):
        trsf_size = 248
        received_file_len = len(self.bin_file)
        print("Current length of the received file :", received_file_len)
        print("Original length of the received file :", original_full_length)
        print("Remaining length of the received file :", remaining_length_of_data_to_receive)

        length_of_blank = (original_full_length - received_file_len) - remaining_length_of_data_to_receive
        empty_packet = bytearray((0xFF,) * trsf_size)
        num_of_empty_packets_needed = int(length_of_blank / trsf_size)

        print("Filling", num_of_empty_packets_needed, "empty packets")
        for i in range(num_of_empty_packets_needed):
            self.bin_file.extend(empty_packet)
        print("New length of the received file :", len(self.bin_file))

    def write_to_file(self, path, data_bytes):
        try:
            with open(path, 'ab') as file:  # Use 'ab' for append mode
                file.write(data_bytes)
            print(f"Bytes successfully appended to '{path}'")
        except Exception as e:
            print(f"Error appending to '{path}': {e}")

    def store_bin_file_as_list(self, path, data_bytes):
        self.bin_file.append(data_bytes)

    def save_file(self):
        path = "bin_file_received.bin"
        with open(path, 'wb') as f:
            f.write(bytes(self.bin_file))


class UpdateHandler:
    ACK_BYTE = 0xCC
    NACK_BYTE = 0x33

    def __init__(self, ser):
        Log.LogAndPrint("Initiating update mode")
        self.ser = ser
        self.original_full_length = 0
        self.sendAck()
        self.fw_bin_file = FirmwareFile()
        while 1:
            self.wait_for_commands_and_reply()

    def sendAck(self):
        time.sleep(waiting_time_before_ack)
        self._write(0x00)
        self._write(0xCC)
        print("Sent ACK message")
        return

    def sendNAck(self):
        time.sleep(waiting_time_before_ack)
        self._write(0x00)
        self._write(0x33)
        return

    def receivePacket(self):
        time.sleep(waiting_time_before_receiving_data)
        got = None
        while not got:
            got = self._read(2)
        size = got[0]  # rcv size
        chks = got[1]  # rcv checksum
        data = bytearray(self._read(size - 2))  # rcv data
        # print("\n\nGot size : %s \t chks : %s \tdata : %s" % (size, chks, binascii.hexlify(data)))
        if len(data) < 10:
            print("\n\nGot size : %s \t chks : %s \tdata : %s" % (size, chks, binascii.hexlify(data)))
        print("*** received %x bytes" % size)

        if chks == sum(data) & 0xFF:
            self.sendAck()
            return data
        else:
            self.sendNAck()
            raise CmdException("Received packet checksum error")

    def _read(self, length):
        barr = bytearray(self.ser.read(length))
        # print("BARR :", barr)
        return barr
        # while 1:
        #     barr = bytearray(self.ser.read(length))
        #     print("BARR :", barr)
        #     if len(barr) > 0:
        #         return barr

    def _write(self, data, is_retry=False):
        if type(data) == int:
            assert data < 256
            goal = 1
            written = self.ser.write(bytes([data]))
        elif type(data) == bytes or type(data) == bytearray:
            goal = len(data)
            written = self.ser.write(data)
        else:
            raise CmdException("Internal Error. Bad data type: {}"
                               .format(type(data)))

        if written < goal:
            print("*** Only wrote {} of target {} bytes".format(written, goal))
            if is_retry and written == 0:
                raise CmdException("Failed to write data on the serial bus")
            print("*** Retrying write for remainder")
            if type(data) == int:
                return self._write(data, is_retry=True)
            else:
                return self._write(data[written:], is_retry=True)

    def sendSuccessResponse(self):
        cmd = commands_ret_dict["COMMAND_RET_SUCCESS"]
        lng = 3

        self._write(lng)  # send size
        self._write(cmd)  # send checksum
        self._write(cmd)  # send data

        print("*** Sent Success Return")
        if self._wait_for_ack("Send Success Return"):
            stat = self.receivePacket()
            return stat

    def _wait_for_ack(self, info="", timeout=1):
        stop = time.time() + timeout
        got = bytearray(2)
        while got[-2] != 00 or got[-1] not in (self.ACK_BYTE,
                                               self.NACK_BYTE):
            got += self._read(1)
            if time.time() > stop:
                raise CmdException("Timeout waiting for ACK/NACK after %s" % timeout)
        print("Got %d additional bytes before ACK/NACK" % (len(got) - 4,))
        ask = got[-1]
        if ask == self.ACK_BYTE:
            # ACK
            return 1
        elif ask == self.NACK_BYTE:
            # NACK
            print("Target replied with a NACK during %s" % info)
            return 0

        # Unknown response
        print("Unrecognised response 0x%x to %s" % (ask, info))
        return 0

    def sendData(self, data):
        lng = len(data) + 2
        self._write(lng)  # send size
        self._write(sum(bytearray(data)) & 0xFF)  # send checksum
        self._write(bytes(data))  # send data
        # print("Response sent :", bytes(data))

    def _decode_addr(self, byte0, byte1, byte2, byte3):
        return (byte3 << 24) | (byte2 << 16) | (byte1 << 8) | (byte0 << 0)

    def _encode_addr(self, addr):
        byte3 = (addr >> 0) & 0xFF
        byte2 = (addr >> 8) & 0xFF
        byte1 = (addr >> 16) & 0xFF
        byte0 = (addr >> 24) & 0xFF
        return bytes([byte0, byte1, byte2, byte3])

    def wait_for_commands_and_reply(self):
        incoming_command = bytes(self.receivePacket())
        if incoming_command[0] in commands_incoming_dict.keys():
            cmd = commands_incoming_dict[incoming_command[0]]
            print("Command Recognised as", cmd)
            if cmd == "MEM_READ":
                print("Requested memory read at address", incoming_command)
                data_to_send = mem_read_data_list[mem_read_address_list.index(incoming_command)]
                print("mem_read_data to send :", data_to_send)
                self.sendData(data_to_send)
                ack_message = str("Mem read read at address : " + str(incoming_command))
                if self._wait_for_ack(ack_message, 10):
                    return

            if cmd == "COMMAND_DOWNLOAD":
                print("\nDownload Command Received")
                starting_address_of_next_data_to_receive = self._decode_addr(incoming_command[4], incoming_command[3],
                                                                             incoming_command[2], incoming_command[1])
                print("Starting_address_of_next_data_to_receive :", starting_address_of_next_data_to_receive)
                remaining_length_of_data_to_receive = self._decode_addr(incoming_command[8], incoming_command[7],
                                                                        incoming_command[6], incoming_command[5])
                if starting_address_of_next_data_to_receive == 0:
                    self.original_full_length = remaining_length_of_data_to_receive
                    print("Original_full_length :", self.original_full_length)
                # print("Remaining_length_of_data_to_receive :", remaining_length_of_data_to_receive, "\n")
                self.fw_bin_file.fillEmptyPackets(self.original_full_length, remaining_length_of_data_to_receive)

            if cmd == "COMMAND_GET_STATUS":
                print("Get Status Command Received")
                response = bytes([0x40])
                self.sendData(response)
                time.sleep(waiting_time_before_sending_response)
                self.sendData(response)
                time.sleep(waiting_time_before_sending_response)
                self.sendData(response)
                time.sleep(waiting_time_before_sending_response)
                self.sendData(response)
                time.sleep(waiting_time_before_sending_response)
                if self._wait_for_ack(str(cmd), 10):
                    return

            if cmd in command_vs_response:
                response = command_vs_response[cmd]
                print("Sending response : " + str(binascii.hexlify(response)))
                time.sleep(waiting_time_before_sending_response)
                self.sendData(response)
                if self._wait_for_ack(str(cmd), 10):
                    return

            if cmd == "COMMAND_SEND_DATA":
                self.fw_bin_file.bin_file.extend(incoming_command[1:])

            if cmd == "COMMAND_CRC32":
                original_file_len = self._decode_addr(incoming_command[8], incoming_command[7], incoming_command[6],
                                                      incoming_command[5])
                print("original_file_len :", original_file_len)

                chksum = self.fw_bin_file.crc32(original_file_len)
                print("\n\nCalculated Checksum :", chksum)

                data = self._encode_addr(chksum)
                self.sendData(data)
                print("Sent Checksum as :", data)
                # print("\n\n\n\nFINAL FILLED BIN FILE\n")
                # print(self.fw_bin_file.bin_file)
                ack_message = "COMMAND CRC32 Executed"
                if self._wait_for_ack(ack_message, 10):
                    return

            if cmd == "COMMAND_RESET":
                print("\n\nUpdate Process Done")
                print('*'*10)
                print("\n\n")

        else:
            print("Command not recognized")
