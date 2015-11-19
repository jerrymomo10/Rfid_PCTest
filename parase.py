from math import log
import time
import sys
import glob
from serial import Serial
from serial import SerialException
# -*- coding:utf-8 -*-
__author__ = 'Jerry'

connected = 0
serial_port = 0
frame_head = 0xffaa  # frame header


def serial_ports():
    """ Lists serial port names
        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(20)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = Serial(port)
            s.close()
            result.append(port)
        except (OSError, SerialException):
            pass
    return result


def connect_serial(port_set="COM1", baud_rate_set=9600):
    global serial_port
    try:
        serial_port = Serial(port=port_set, baudrate=baud_rate_set)
    except (OSError, SerialException):
        return False
    global connected
    connected = 1
    return True

def send_frame(data, repeat=1):
    if data == 0:
        length = 1
    else:
        length = int(log(data, 256))+1
    lister = []
    # add the data
    for i in range(length):
        bitwise = 0xff << i*8
        lister.append(chr((data & bitwise) >> 8*i))  # 8 bit convert
    # add the head
    head_length = int(log(frame_head, 256))+1
    for i in range(head_length):
        bitwise = 0xff << i*8
        lister.append(chr((frame_head & bitwise) >> 8*i))
    lister.reverse()
    # add the checksum 1byte
    check_sum = ord(lister[0])
    for c in lister:
        if c is not lister[0]:
            check_sum ^= ord(c)
    lister.append(chr(check_sum))
    # send to the serial
    if connected == 1:
        for i in range(int(repeat)):
            serial_port.write(lister)
            time.sleep(0.001)


def receive_data():
    reads = []
    if connected:
        while serial_port.inWaiting() > 0:
            if serial_port.inWaiting() > 0:
                reads.append(ord(serial_port.read(1)))
            time.sleep(0.001)
    return reads








