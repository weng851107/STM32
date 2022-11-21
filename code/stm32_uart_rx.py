#!/opt/python_3.8.9_arm/bin/python3
# -*- coding:utf-8 -*-

import threading
import time
import serial

import sys

PORT="/dev/ttyS1"
BAUDRATE=115200

# global variable
ser = None

def init_serial():
	global ser
	
	'''
	## comment out this code for tx during rx
	'''
	#if _ser != None:
	#	print("Serial is opened, please wait...")
	#	return None

	ser = serial.Serial(PORT, BAUDRATE, 8, 'N', 1)
	ser.flushInput()
	ser.flushOutput()
	return ser

class SerialPortReadThread(threading.Thread):
	def __init__(self, _ser, _port, _baudrate):
		threading.Thread.__init__(self)
		self.port = _port
		self.baudrate = _baudrate

		self.ser = _ser		#serial.Serial(self.port, self.baudrate, 8, 'N', 1)
		self.ser.flushInput()
		self.ser.flushOutput()

	def run(self):
		while True:
			resp = self.ser_readline()
			print(resp[:-1])

	def ser_write(self, cmd):
		self.ser.write(cmd.encode())

	def ser_readline(self):
		resp = self.ser.readline().decode('ascii')
		return resp

	def ser_close(self):
		if self.ser != None:
			self.ser.flushInput()
			self.ser.flushOutput()
			self.ser.close()

if __name__ == '__main__':
	ser = init_serial()

	read_thread = SerialPortReadThread(ser, PORT, BAUDRATE)

	read_thread.start()
	read_thread.join()


