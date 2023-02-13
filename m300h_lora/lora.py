"""
@author: Abdelrahman Mahmoud Gaber
@email: abdulrahman.mahmoud1995@gmail.com
"""
#%%
from serial_communication import *
from commands import *

"""
TODO:
    1. create the listener thread
    2. AT-COMMAND reader Class 
    3. 

"""

class Lora(SerialCommunication):
    def __init__(self, port, baudrate, timeout=1, debug=True):
        super().__init__(port, baudrate, timeout, debug)

        self._sending_timeout = timeout
        self._status = StatusNetwork.RESET # defualt 
    
    @property
    def status(self):
        return self._status

    def send_raw_command(self, command):
        """
        Send raw command to the LoRa module.

        param: command: str
        """
        # TODO
        #   1. stop the thread from reading the coming data .. 
        # clear all coming data if any
        command = command.serialize().encode()
        # timer = time.time()
        while self.is_available:
            # for debugging
            print("----------FOUND IN BUFFER------------")
            print(self.readlines())
            print("-------------------------------------")
            # if time.time() - timer > self._sending_timeout:
            #     raise Exception("Couldn't clear the buffer")
        self.send(command)
        return 
lora = Lora("COM12", 9600, timeout=0.1) #/dev/ttyUSB1
lora.connect()

#%%
# lora.connect()
lora.send(b"AT+DIOSLEEP=?\r\n")
time.sleep(0.1)
print("coming data: ",  lora.is_available)
data = lora.readlines()
print(data)
#%%



time.sleep(0.1)
print("coming data: ",  lora.is_available)
data = lora.readlines()
print(data)

name, mode, payload = Command.command_check(data[1]) 
lrrecv = Command.construct_from_payload(name, mode, payload)
#print(lrrecv.data[1])
print(vars(lrrecv))


# lora = Lora("/dev/ttyUSB1", 9600, timeout=0.1)
# lora.connect()
# lrsend = Command("LRSEND", SET, port=33, confirm=0, len=33, data="<abcdef")
# # status = Command("STATUS", GET)
# # devinfo = Command("DEVINFO", GET)
# # lora.send_raw_command(devinfo)
# # lora.send_raw_command(status)
# lora.send_raw_command(lrsend)

# time.sleep(0.1)
# print("coming data: ",  lora.is_available)
# data = lora.readlines()
# print(data)

# n, m, p = Command.command_check(b'+DEVINFO:"M100C  FW VER:0.99.78  HW VER:1.01(H)  BOOT VER:0.99.14  LORAWAN VER:1.0.2  REGION:AS923"\r\n'.decode().strip())
# dev_info = Command.construct_from_payload(n, m, p)
# print(vars(dev_info))
# dev_info.info
