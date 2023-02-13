#!/usr/bin/env python3
#%% -*- coding: utf-8 -*-
"""
@author: Abdelrahman Mahmoud Gaber
@email: abdulrahman.mahmoud1995@gmail.com
"""
from m300h import *

from enum import IntEnum
import re

class Command:
       
    def __init__(self, name, mode=GET, **kwargs):
        """
        Constructor for AT Commands that user can send. 
        
        .. NOTE::
            This constructor valid only(to set attributes) for GET, SET, EXECUTE commands.
            REPORT however will have a special method to handle it. 
        
        :param name: name of the command (for example: LRSEND, LRCONFIRM)
        :param mode: command mode e.g. GET, SET, EXECUTE  or REPORT
        :param kwargs: if command fields need to be added for example(port=12, seq=365, and so on)
        """
        self.name = name # command name
        self._payload = ""
        self._mode = mode
        self._mode_str = GET_STR
        
        if self._mode == SET:
            self._mode_str = SET_STR
        elif self._mode == EXECUTE:
            self._mode_str = EXECUTE_STR
        elif self._mode == REPORT:
            self._mode_str = ""
        
        # check if name ends of numbers
        regex = r"^[0-9A-Z][A-Z]+([0-9]+)$" # to get the number at the end
        self.base_name = self.name # to keep the original name
        if self.name[-1].isdigit():
            match = re.match(regex, self.name)
            if match is not None:
                self.base_name = self.name[:-len(match.groups()[0])]
            else:
                raise CommandError("Invalid command name {name}".format(name=self.name))         

        if self.base_name not in (*AT_COMMANDS, *AT_COMMANDS_REPORT): # make sure command is defined
            raise CommandNotFoundError("Command not found or not defined")

        if self._mode not in (GET, SET, EXECUTE, REPORT):
            raise CommandError("Invalid command mode {mode} - must be GET, SET or EXECUTE")
        
        if self._mode == SET: # fields are present only when SET command for REPORT a special method is used
            self._set_attributes(**kwargs) # set , command fields

    def _set_attributes(self, **kwargs):
        """
        This method is used to set command fields such as port, seq, len, etc.
        """

        # check which dictionary the command belongs to



        fields_list = AT_COMMANDS[self.base_name] # defualt fields defined in AT_COMMAND
        fields_passed = kwargs.keys()
        if len(kwargs) == 0: # if no kwargs, assume all fields are null (normal value)
            self._set_default_attribute()
            return
        else:
            for field in fields_list:
                if field[0] in fields_passed:
                    try:
                        setattr(self, field[0], field[1](kwargs[field[0]]))
                    except CommandError:
                        raise CommandError("Invalid field type {type}".format(type=field[1]))
                else:
                    try:
                        setattr(self, field[0], field[1]())
                    except CommandError:
                        raise CommandError("Invalid field type {type}".format(type=field[1]))

    def _set_default_attribute(self):
        
        fields_list = AT_COMMANDS_REPORT[self.base_name] if self._mode == REPORT else AT_COMMANDS[self.base_name]
        for field in fields_list:
            try:
                setattr(self, field[0], field[1]())
            except CommandError:
                raise CommandError("Invalid field type {type}".format(type=field[1]))
    
    def serialize(self):
        """
        This method is used to serialize(convert to string) AT command to send to the gateway.
        """
        # construct the payload first
        self._payload = "" if self._mode != REPORT else "" # initialize payload
        if self._mode == REPORT: # TODO: check doesn't make sense?
            return "^" + self.name + "=" + self._payload 
        if self._mode == GET:
            self._payload = ""
        elif self._mode == SET:
            fields_list = AT_COMMANDS[self.base_name]
            for field in fields_list:
                self._payload += str(getattr(self, field[0])) + ","
            self._payload = self._payload[:-1] # remove last comma
        elif self._mode == EXECUTE:
            self._payload = ""
        
        cmd_str = AT_CMD_PREFIX + self.name + self._mode_str + self._payload + CRLF
        return cmd_str

    @staticmethod 
    def construct_from_payload(command_name, mode, payload):
        """
        This method is used to for parsing the received data.

        :param command_name: name of the command
        :param type: command type (REPORT or others)
        :param payload: data received from the device
        """

        command = Command(command_name, mode=mode)
        command._payload = payload
        base_name = command.base_name
        fields_list = AT_COMMANDS_REPORT[base_name] if mode == REPORT else AT_COMMANDS[base_name] 
        for idx, field in enumerate(fields_list):
            if field[0] == "data": # TODO: check if this is the best way to handle data 
                payload[idx] = payload[idx].replace("<", "")
            command.__setattr__(field[0], field[1](payload[idx]))
        return command               

    @staticmethod
    def command_check(command_str):
        """
        Check if data contains AT Commands, if found return (command_name, command_mode, payload).
        
        .. NOTE::
            Make sure command_str is already decoded and doesn't have \r\n

        :returns:
            :command_name: name of the command
            :command_mode: mode of the command (REPORT or others)
            :payload: command payload
        """

        command_str = command_str.decode("utf-8").strip() # decode and remove \r\n
        command_name, command_mode, payload_index = None, None, None
        match = re.match(COMMAND_CHANNEL_REGEX, command_str)
        if match: # check if command is channel command
            command_name = match.groups()[0] + match.groups()[1]
        else:
            match = re.match(COMMAND_REGEX, command_str)
            if match is None:
                return None, None, None
            command_name = match.groups()[0]
        command_mode = REPORT if command_str.startswith("^") else GET # we only care about REPORT here
        payload_index = match.regs[0][1]
        payload = command_str[payload_index:].split(",")
        return command_name, command_mode, payload

    @staticmethod
    def parse(command_str):
        """
        This method is used to parse the received data.

        :param command_str: data received from the device
        """

        command_name, command_mode, payload = Command.command_check(command_str)
        if command_name is None:
            return None
        return Command.construct_from_payload(command_name, command_mode, payload)
    
    def __getitem__(self, name):
        """
        This method is used to get the value of the field.
        """
        try:
            return self.__dict__[name]
        except KeyError:
            raise AttributeError(name)
        
    def __str__(self):
        """
        return a string representation of the command.
        For example: LRSEND Command will be
            LRSEND(mode=SET, payload={port=33, confirm=1, len=36, data=12396895})
        """

        name = self.name
        mode = COMMAND_TYPES_STR[self._mode]
        fields_list = AT_COMMANDS_REPORT[self.base_name] if self._mode == REPORT else AT_COMMANDS[self.base_name]
        payload = ""
        for field in fields_list:
            payload += str(field[0]) + "=" + str(getattr(self, field[0])) + ", "
        payload = payload[:-2] # remove last comma
        return "{name}(mode={mode}, payload=[{payload}])".format(name=name, mode=mode, payload=payload)
    
    def __repr__(self):
        return self.__str__()

#%% Testing from payload (for msg recived)
# command_raw = b"^LRRECV:1,22,-44,29,2,<ABCD,923.2,2\r\n"
# command_raw = "^LRJOIN:481.5,0"
# command_raw = "^LRCONFIRM:1,-128,10,481.5,0"
# name, mode, payload = Command.command_check(command_raw) 
# print("name: ", name, "\nmode: ", mode, "\npayload: ", payload)
# lrrecv = Command.parse(command_raw)
# print(lrrecv)
# print(lrrecv["data"])

#%%
# AT+MULTICAST0=1,0xFFFFFFFF,>FEEDDCC8C7FC6CBC33D0809FB565001,>F Set the multicast address
# EEDDCC8C7FC6CBC33D0809FB565002,0
multicast = Command("MULTICAST25", GET, s=1, addr="0xFFFFFFFF", appskey=">FEEDDCC8C7FC6CBC33D0809FB565001", nwkskey=">FEEDDCC8C7FC6CBC33D0809FB565002", seq=0)
multicast.serialize()

command_raw = b'+MULTICAST56:1,0xFFFFFFFF,>FFEEDDCC8C7FC6CBC33D0809FB565001,>FFEEDDCC8C7FC6CBC33D0809FB565002,0\r\n'
multicast = Command.parse(command_raw)
print(multicast)
# lrconfirm = Command.construct_from_payload(name, mode, payload)
# print(lrrecv.data)
# print(vars(lrrecv))

# #%% Testing 
# lrsend = Command("LRSEND", SET, port=33, confirm=1, len=36, data="12396895")

# print(lrsend.serialize())
# vars(lrsend)

# lrnsend = Command("LRNSEND", SET)
# status = Command("STATUS", GET)
# print(status.serialize())
# vars(lrsend)

# device_class = Command("DEVCLASS", SET)
# vars(device_class)
# #%% Test serilzation
# lrsend = Command("LRSEND", SET, port=33, confirm=0, len=33, data="<abcdef")
# print(lrsend.serialize())

# status = Command("STATUS", GET)
# print(status.serialize())

# device_class = Command("DEVCLASS", SET)
# print(device_class.serialize())





# %%
