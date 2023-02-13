"""
@author: Abdelrahman Mahmoud Gaber
@email: abdulrahman.mahmoud1995@gmail.com
"""

from enum import IntEnum
# command types 
SET = 0
GET = 1
EXECUTE = 2
REPORT = 3 # ^X:P report command, P is the parameter e.g. '^LRRECV:1,22,-44,29,2,<ABCD,923.2,2\r\n'

# dictionary of commands types
COMMAND_TYPES_STR = {
    SET: "SET",
    GET: "GET",
    EXECUTE: "EXECUTE",
    REPORT: "REPORT"
}

SET_STR = "="
GET_STR = "=?"
EXECUTE_STR = ""
REPORT_STR = ""

CR = "\r"
LF = "\n"
CRLF = "\r\n"

AT_CMD_PREFIX = "AT+"

COMMAND_REGEX = r"(?:\^|\+)([0-9A-Z]+[A-Z]+):" # command regex to check if data contains a command
COMMAND_CHANNEL_REGEX = r"(?:\^|\+)([0-9A-Z]*[A-Z]+)([0-9]+):"

AT_COMMANDS = { # for query, setup 

    "LRSEND" : ( 
        ("port"   , int),
        ("confirm", int),
        ("len"    , int),
        ("data"   , str) # TODO: convert to bytes
    ),

    "LRNSEND" : ( # port, confirm, nbtrials, len, data
        ("port"    , int),
        ("confirm" , int),
        ("nbtrials", int),
        ("len"     , int),
        ("data"    , str) # TODO: convert to bytes
    ),

    "DEVINFO" : (
        ("info", str),
    ),

    "REGION" : ( 
        ("region", str),
    ),

    "DEVCLASS": (
        ("class", int),
    ),
    
    "STATUS": (
        ("status", int),
    ),

    "ACTIVEMODE": (
        ("mode", int),
    ),

    "APPEUI": (
        ("mode", str),
    ),

    "DEVEUI": (
        ("mode", str),
    ),

    "APPKEY": (
        ("mode", str),
    ),

    "ADREN": (
        ("mode", int),
    ),

    "DUTYCYCLEEN": (
        ("mode", int),
    ),

    "CONFTCNT": (
        ("mode", int),
    ),

    "UCONFTCNT": (
        ("mode", int),
    ),

    "MULTICASTALL": ( #AT+ MULTICASTALL=?
        ("mode", int), 
    ),

    "DEFAULTPW": (
        ("mode", int),
    ),

    "CURRENTPW": (
        ("mode", int),
    ),

    "DEFAULTDR": (
        ("pw", int),
    ),

    "CURRENTDR": (
        ("mode", int),
    ),
    
    "CHANDIS": ( # SET Only
        ("mode", int),
    ),
    
    "CHANGROUP": ( # SET Only
        ("mode", int),
    ),

    "CURRENTCHANALL": ( 
        ("mode", int),
    ),
   
    "CHANMASKALL": ( 
        ("mode", int),  
    ),

    "RX2CHAN": ( 
        ("mode", int),  
    ),

    "DIOSLEEP": ( 
        ("mode", int),  
    ),

    "CURRENTCHANALL": ( # x, freq, dr_min, dr_max, s, band, dutycycle  (AS923)
        ("x" , int),  #Range: 0 to 15 (AS923), 0 to 71 (AU915), 0 to 95 (CN470), 0 to 15 (EU868), 0 to 15 (IN864), 0 to 15 (KR920), 0 to 15 (RU864), 0 to 71 (US915).
        ("freq", float),   #WFrequency, floating-point number, unit MHz
        ("dr_min" , int), #Range: 0 to 7 (AS923), 0 to 7 (EU868), 0 to 7 (IN865), 0 to 5 (KR920).
        ("dr_max", str), #Range: 0 to 7 (AS923), 0 to 7 (EU868), 0 to 7 (IN865), 0 to 5 (KR920).
        ("s"  , int),   #Whether the channel is enabled 0: Not enabled 1: Enable
        ("band"  , int),  #The band number, integer, where the channel is located
        ("dutycycle"  , int)  #The band number, integer, where the channel is located
    ),

    "RX2CHAN": ( # freq, dr  (AS923)
        ("freq" , float),  #WFrequency, floating-point number, unit MHz
        ("dr", int)   #Default values: 2 (AS923), 8 (AU915), 0 (CN470), 0 (EU868), 2 (IN865), 0 (KR920), 0 (RU864), 8 (US915).
    ),
    
    "DIOSLEEP": ( # freq, dr  (AS923)
        ("freq" , float),  #WFrequency, floating-point number, unit MHz
        ("dr", int)   #Default values: 2 (AS923), 8 (AU915), 0 (CN470), 0 (EU868), 2 (IN865), 0 (KR920), 0 (RU864), 8 (US915).
    ),

#   COMMANDS WITH CHANNELS

    "CHANMASK": ( # x, mask  (AS923)
        ("mask", int)   #Channel enable mask, integer, range 0x0000 to 0xFFFF
    ),

    "CHAN": ( # x, freq, dr_min, dr_max, s, band, dutycycle  (AS923)
        ("freq", float),   #WFrequency, floating-point number, unit MHz
        ("dr_min" , int), #Range: 0 to 7 (AS923), 0 to 7 (EU868), 0 to 7 (IN865), 0 to 5 (KR920).
        ("dr_max", str), #Range: 0 to 7 (AS923), 0 to 7 (EU868), 0 to 7 (IN865), 0 to 5 (KR920).
        ("s"  , int),   #Whether the channel is enabled 0: Not enabled 1: Enable
        ("band"  , int), #The band number, integer, where the channel is located
        ("dutycycle"  , int)  #The band number, integer, where the channel is located
    ),

    "MULTICAST": ( # x, s, addr, appskey, nwkskey, seq
        ("s", int),   #Whether the multicast address is enabled, integer, range 0 to 1
        ("addr" , str), #The short address used by this multicast address ranges from 0x00 to 0xFFFFFFFF
        ("appskey", str), #The multicast address uses APPSKEY, block type, 16 bytes
        ("nwkskey"  , str),   #The multicast address uses NWKSKEY, block type, 16 bytes
        ("seq"  , str)  #The serial number currently used by the multicast address, an integer, ranges from 0 to 0xFFFFFFFF
    ),
}

AT_COMMANDS_REPORT = {
    "LRSEND": (
        ("seq"    , int),
        ("port"   , int),
        ("confirm", int),
        ("len"    , int),
        ("freq"   , float),
        ("dr"     , int)
    ),

    "LRRECV": (
        ("seq" , int),
        ("port", int),
        ("rssi", int),
        ("snr" , int),
        ("len" , int),
        ("data", str),
        ("freq", float),
        ("dr"  , int)
    ),

    "LRCONFIRM": ( # seq, rssi, snr, freq, dr
        ("seq" , int),
        ("rssi", int),
        ("snr" , int),
        ("freq", float),
        ("dr"  , int)
    ),

    "LRJOIN": (
        ("freq", float),
        ("dr"  , int),
    ),

    "STATUS": ( 
        ("status", int),
    ),
}


# status network enum
class StatusNetwork(IntEnum):
    RESET = 0
    P2P_NETWORK = 1
    NOT_JOINED = 2
    OTAA_JOINED = 3
    ABP_JOINED = 4

class DevClass(IntEnum):
    CLASS_A = 0
    CLASS_B = 1
    CLASS_C = 2

class DevClassStatus(IntEnum):
    OK = 0
    ERROR = 1

class ActiveMode(IntEnum):
    OTAA = 0
    ABP = 1 
    OTAA_RPM = 2 

class ADRFunction(IntEnum):
    ADRDISABLE = 0
    ADRENABLE = 1 

class DutyCycle(IntEnum):
    DUTYCYCLEDISABLE = 0
    DUTYCYCLEENABLE = 1 

class DefaultPower(IntEnum):
    DBM_16 = 0
    DBM_14 = 1
    DBM_12 = 2
    DBM_10 = 3
    DBM_8 = 4
    DBM_6 = 5
    DBM_4 = 6
    DBM_2 = 7 

class CurrentPower(IntEnum):
    DBm_16 = 0
    DBm_14 = 1
    DBm_12 = 2
    DBm_10 = 3
    DBm_8 = 4
    DBm_6 = 5
    DBm_4 = 6
    DBm_2 = 7     
     
class DefaultADR(IntEnum):
    DR_0 = 0
    DR_1 = 1
    DR_2 = 2
    DR_3 = 3
    DR_4 = 4
    DR_5 = 5
    DR_6 = 6
    DR_7 = 7 

class CurrentADR(IntEnum):
    DR_0 = 0
    DR_1 = 1
    DR_2 = 2
    DR_3 = 3
    DR_4 = 4
    DR_5 = 5
    DR_6 = 6
    DR_7 = 7     
           

ActiveModeMsg = {
    0: "OTAA network access mode",
    1: "ABP network access mode",
    2: "After OTAA is connected to the network, switch to ABP network access mode"
}

StatusMsg = {
    0: "Reset",
    1: 'In the P2P communication state',
    2: 'In the LORAWAN state is not joined to the network',
    3: "In LORAWAN OTAA mode and already in the network status",
    4: "In LORAWAN ABP mode and already in the network status"
}

ErrorMsg = {
    1 : "The number of AT command characters exceeds the range",
    2 : "Unknown command that is not recognized",
    3 : "The command is not allowed to be executed",
    4 : "Parameter format or type error",
    5 : "The parameter is out of range",
    6 : "The length of the block parameter or string parameter exceeds the range",
    7 : "The LORAWAN data send queue is full",
    10 : "The module is not activated"
}
ADRFunctionMsg = {
    0: "The ADR function is not enabled",
    1: "Enable the ADR function"
}
DutyCycleMsg = {
    0: "Does not enable DUTYCYCLE function",
    1: "Enables DUTYCYCLE function"
}
DefaultADRMsg = {
    0 : "DR_0(SF12 BW125K)",
    1 : "DR_1(SF11 BW125K)",
    2 : "DR_2(SF10 BW125K)",
    3 : "DR_3(SF9 BW125K)",
    4 : "DR_4(SF8 BW125K)",
    5 : "DR_5(SF7 BW125K)",
    6 : "DR_6(SF7 BW250K)",
    7 : "DR_7(FSK 50K)"
}
CurrentADRMsg = {
    0 : "DR_0(SF12 BW125K)",
    1 : "DR_1(SF11 BW125K)",
    2 : "DR_2(SF10 BW125K)",
    3 : "DR_3(SF9 BW125K)",
    4 : "DR_4(SF8 BW125K)",
    5 : "DR_5(SF7 BW125K)",
    6 : "DR_6(SF7 BW250K)",
    7 : "DR_7(FSK 50K)"
}
class CommandNotFoundError(Exception):
    """
    Exception for when a command is not found or defined in AT commands
    """
    pass

class CommandError(Exception):
    """
    command is not properly formatted or defined or has invalid fields
    """
    pass

