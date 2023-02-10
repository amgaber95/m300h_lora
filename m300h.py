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

SET_STR = "="
GET_STR = "=?"
EXECUTE_STR = ""
REPORT_STR = ""

CR = "\r"
LF = "\n"
CRLF = "\r\n"

AT_CMD_PREFIX = "AT+"

COMMAND_REGEX = r"(?:\^|\+)([A-Z0-9]*):" # command regex to check if data contains a command

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
        ("region", int),
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
    ABP = 1 # gps detected 
    OTAA_RPM = 2 

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

