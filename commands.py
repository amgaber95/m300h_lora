#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
        
        if self.name not in (*AT_COMMANDS.keys(), *AT_COMMANDS_REPORT): # make sure command is defined
            raise CommandNotFoundError("Command not found or not defined")

        if self._mode not in (GET, SET, EXECUTE, REPORT):
            raise CommandError("Invalid command mode {mode} - must be GET, SET or EXECUTE")
        
        if self._mode == SET: # fields are present only when SET command for REPORT a special method is used
            self._set_attributes(**kwargs) # set , command fields

    def _set_attributes(self, **kwargs):
        """
        This method is used to set command fields such as port, seq, len, etc.
        """

        fields_list = AT_COMMANDS[self.name] # defualt fields defined in AT_COMMAND
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
        
        fields_list = AT_COMMANDS_REPORT[self.name] if self._mode == REPORT else AT_COMMANDS[self.name]
        for field in fields_list:
            try:
                setattr(self, field[0], field[1]())
            except CommandError:
                raise CommandError("Invalid field type {type}".format(type=field[1]))
    
    def serilize(self):
        """
        This method is used to serilize(convert to string) AT command to send to the gateway.
        """
        # construct the payload first
        self._payload = "" if self._mode != REPORT else "" # intialize payload
        if self._mode == REPORT: # TOCHECK doesn't make sense
            return "^" + self.name + "=" + self._payload 
        if self._mode == GET:
            self._payload = ""
        elif self._mode == SET:
            fields_list = AT_COMMANDS[self.name]
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
        This method is used to for parsing the recived data.

        :param command_name: name of the command
        :param type: command type (REPORT or others)
        :param payload: data recived from the device
        """

        command = Command(command_name, mode=mode)
        command._payload = payload

        fields_list = AT_COMMANDS_REPORT[command_name] if mode == REPORT else AT_COMMANDS[command_name] 
        for idx, field in enumerate(fields_list):
            if field[0] == "data": # TOCHECK 
                payload[idx] = payload[idx].replace("<", "")
            command.__setattr__(field[0], field[1](payload[idx]))
        return command               

    @staticmethod
    def command_check(command_str):
        """
        Check if data contains AT Commands, if found return (command_name, payload).
        
        .. NOTE::
            Make sure command_str is already decoded and doesn't have \r\n

        :returns:
            :command_name: name of the command
            :command_mode: mode of the command (REPORT or others)
            :payload: command payload
        """
        match = re.match(COMMAND_REGEX, command_str)
        if match is None:
            return None, None, None
        command_name = match.groups()[0]
        command_mode = REPORT if command_str.startswith("^") else GET # we only care about REPORT here
        payload_index = match.regs[0][1]
        payload = command_str[payload_index:].split(",")
        return command_name, command_mode, payload


# #%% Testing from payload (for msg recived)
# command_raw = "^LRRECV:1,22,-44,29,2,<ABCD,923.2,2\r\n".strip()
# command_raw = "^LRJOIN:481.5,0"
# command_raw = "^LRCONFIRM:1,-128,10,481.5,0"
# name, mode, payload = Command.command_check(command_raw) 
# print("name: ", name, "\nmode: ", mode, "\npayload: ", payload)
# lrrecv = Command.construct_from_payload(name, mode, payload) 
# lrconfirm = Command.construct_from_payload(name, mode, payload)
# print(lrrecv.data)
# print(vars(lrrecv))

# #%% Testing 
# lrsend = Command("LRSEND", SET, port=33, confirm=1, len=36, data="12396895")

# print(lrsend.serilize())
# vars(lrsend)

# lrnsend = Command("LRNSEND", SET)
# status = Command("STATUS", GET)
# print(status.serilize())
# vars(lrsend)

# device_class = Command("DEVCLASS", SET)
# vars(device_class)
# #%% Test serilzation
# lrsend = Command("LRSEND", SET, port=33, confirm=0, len=33, data="<abcdef")
# print(lrsend.serilize())

# status = Command("STATUS", GET)
# print(status.serilize())

# device_class = Command("DEVCLASS", SET)
# print(device_class.serilize())


