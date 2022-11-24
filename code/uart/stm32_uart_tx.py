#!/opt/python_3.8.9_arm/bin/python3
# -*- coding:utf-8 -*-

import os
import serial
import time
import threading


# version of this test script
VERSION = 0.1
PORT="/dev/ttyS1"
BAUDRATE=115200

# global variable
ser = None

mutex = threading.Lock()

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

def _main():
	global ser
	global mutex

	ser = init_serial()
	while True:

		__cmd = input("input:")

		if 'q' in __cmd and len(__cmd) == 1:
			break

		if ser != None:
			cmd = "CMD:" + str(__cmd) + "~END"
			print("cmd = ", cmd)
			mutex.acquire()
			os.system("echo 1 > /tmp/.stm32_uart_flag")
			ser.write(cmd.encode())
			os.system("echo 0 > /tmp/.stm32_uart_flag")
			mutex.release()

	close_serial(ser)
	ser = None

if __name__ == '__main__':
	_main()



