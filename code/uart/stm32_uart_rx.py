#!/opt/python_3.8.9_arm/bin/python3
# -*- coding:utf-8 -*-

import threading
import time
import serial

import sys
import os

PORT="/dev/ttyS1"
BAUDRATE=115200

# global variable
ser = None

mutex = threading.Lock()

def init_serial():
	global ser
	global mutex

	mutex.acquire()
	os.system("echo 0 > /tmp/.stm32_uart_flag")
	mutex.release()

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
		global mutex
		while True:
			mutex.acquire()
			fp = os.popen("cat /tmp/.stm32_uart_flag")
			flag = fp.read()
			fp.close()
			mutex.release()
			if '0' in flag:
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


