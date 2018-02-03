#!/usr/bin/python
import os
import sys
import socket
from subprocess import call, check_output
import pexpect
import time

class Light:
    "Light class to allow interaction with the Beewi bluetooth bulb"

    # Default values
    bulb_mac = "B4:99:4C:59:EB:13"
    default_status = "off"

    def __init__(self):
        # Set MAC address of the bulb (bluetooth)
        self.mac = Light.bulb_mac
        print "Light mac: " + self.mac

        # Set default status ON/OFF
        if Light.default_status == "on":
            self.switchBulbOn()
        else:
            self.switchBulbOff()

        # Get bulb settings
        self.settings = self.getSettings()

        # Set brightness to default
        #self.brightness = ScrollpHatHD.default_brightness
        #print "Screen brightness: " + str(self.brightness)

    def getSettings(self):
        # read the settings characteristic (read handle is 0x0024)
        # command return value = 'Characteristic value/descriptor: 00 b2 ff 00 00'
        # function returns settings as array of five integers
        self.cycleHCI();
        settings_array = [0,0,0,0,0]
        raw_input=check_output(['gatttool', '-i', 'hci0', '-b', self.mac, '--char-read', '--handle=0x0024']);
        if ':' in raw_input:
            raw_list=raw_input.split(':')
            raw_data=raw_list[1]
            raw_data=raw_data.strip()
            octet_list=raw_data.split(' ')
            if len(octet_list) > 4 :
                for i in range(0, 5) :
                    j = int(octet_list[i], 16)
                    settings_array[i] = j
        return settings_array

    def cycleHCI(self):
        # maybe a useless time waster but it makes sure our hci0 is starting fresh and clean
        # nope in fact we need to call this before each time we do hci or gatt stuff or it doesn't work
        call(['hciconfig', 'hci0', 'down'])
        time.sleep(0.1)
        call(['hciconfig', 'hci0', 'up'])
        time.sleep(0.1)

    def writeCommandToBulb(self, cmd):
        # settings commands are sent to the 0x0021 characteristic
        # all commands are prefixed with 0x55 (85) and suffixed with 0x0d 0x0a (CR LF)
        if cmd != '' :
            cmd = '55' + cmd + '0D0A'
            self.cycleHCI()
            hd = check_output(['/usr/bin/hcitool', '-i', 'hci0', 'lecc', self.mac])
            ha = hd.split(' ');
            connectionHandle=0
            if ha[0] == 'Connection' and ha[1] == 'handle': 
                connectionHandle = ha[2]
            if connectionHandle > 0 :
                bulb = pexpect.spawn('gatttool -i hci0 -b ' + self.mac + ' -I')
                bulb.expect('\[LE\]>', timeout=60)
                bulb.sendline('connect')
                bulb.expect('\[LE\]>', timeout=60)
                bulb.sendline('char-write-cmd 0x0021 ' + cmd)
                bulb.expect('\[LE\]>', timeout=60)
                bulb.sendline('disconnect')
                bulb.expect('\[LE\]>', timeout=60)
                bulb.sendline('exit')
                bulb.expect(pexpect.EOF, timeout=60)
                call(['hcitool', '-i', 'hci0', 'ledc', connectionHandle])
            self.cycleHCI()

    def setBrightness(self, value):
        # brightness command is 12 [02 to 0B] (18, [2 to 11])
        if value == 'low' :
            self.writeCommandToBulb('1202')
        elif value == 'med' :
            self.writeCommandToBulb('1207')
        else :
            self.writeCommandToBulb('120B')

    def setBulbColour(self, colour):
        # colour command is 13 RR GG BB (19, Red, Green, Blue)
        value = '13' + colour
        self.writeCommandToBulb(value)
        return

    def switchBulb(self):
        if self.status == "on":
            self.switchBulbOff()
        else:
            self.switchBulbOn()
        return

    def switchBulbOn(self):
        # on command is 10 01 (16, 1)
        self.writeCommandToBulb('1001')
        self.status = "on"
        return

    def switchBulbOff(self):
        # off command is 10 00 (16, 0)
        self.writeCommandToBulb('1000')
        self.status = "off"
        return