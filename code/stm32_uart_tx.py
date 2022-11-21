#!/opt/python_3.8.9_arm/bin/python3
# -*- coding:utf-8 -*-

import os
import serial
import time


# version of this test script
VERSION = 0.1
PORT="/dev/ttyS1"
BAUDRATE=115200

# global variable
ser = None

def init_serial():
	global ser
	if ser != None:
		print("Serial is opened, please wait...")
		return None

	ser = serial.Serial(PORT, BAUDRATE, 8, 'N', 1)
	ser.flushInput()
	ser.flushOutput()
	return ser

def close_serial(ser):
	if ser != None:
		ser.flushInput()
		ser.flushOutput()
		ser.close()

uart = serial.Serial(PORT, BAUDRATE, 8, 'N', 1)

def _main():
	global ser

	__cmd = input("input:")

	ser = init_serial()
	if ser != None:
		cmd = str(__cmd)
		ser.write(cmd.encode())
		close_serial(ser)

if __name__ == '__main__':
	_main()
	uart.close()


