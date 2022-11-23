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

	ser = serial.Serial(PORT, BAUDRATE, 8, 'N', 1, timeout=1)
	ser.flushInput()
	ser.flushOutput()
	return ser

def close_serial(ser):
	if ser != None:
		ser.flushInput()
		ser.flushOutput()
		ser.close()

def _main():
	global ser

	while True:

		__cmd = input("input:")

		ser = init_serial()
		if ser != None:
			cmd = "CMD:" + str(__cmd) + "~END"
			print("cmd = ", cmd)
			ser.write(cmd.encode())
			while True:
				resp = ser.readline().decode('ascii')
				print(resp[:-1])
				if len(resp) == 0:
					break
			close_serial(ser)
			ser = None

if __name__ == '__main__':
	_main()
