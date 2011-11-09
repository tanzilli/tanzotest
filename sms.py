#!/usr/bin/python

import serial
import time

send_to = "+3940916"
message = "Test"

ser = serial.Serial(
	port='/dev/ttyS1', 
	baudrate=115200, 
	timeout=1,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS
)
ser.flushOutput()
ser.flushInput()

ser.write("ATH\r")
print ser.readlines()
 
ser.write("AT+CMGF=1\r")
print ser.readlines()

ser.write("AT+CMGL=0\r")
print ser.readlines()

ser.write("AT+CMGS=" + "\"" + send_to + "\"" + "\r")
time.sleep(0.5);
ser.write(message + "\x1a")
time.sleep(1);
print ser.readlines()

ser.close()
