#!/usr/bin/python

# Banco di Test per Multicon Gateway ACME-0011
# Lanciare su un PC Linux dotato di porta seriale di debug

import serial
import time
import sys
import getopt
import string 
import datetime
import select
import termios
import sys
import tty

def isData():
	return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])


color_warning = "\x1B[30;41m" 
color_pass = "\x1B[30;42m" 
color_normal = "\x1B[0m" 

serialdevice = "/dev/ttyUSB0"

print "Banco di Test Arietta con WiFi"


#Open the serial port 
ser = serial.Serial(
	port=serialdevice, 
	baudrate=115200, 
	timeout=0.1,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS
)  
ser.flushInput()
old_settings = termios.tcgetattr(sys.stdin)

print "Caratteri in ricezione dalla DebugPort (type Ctrl-C to exit)"

token=""
try:
	tty.setcbreak(sys.stdin.fileno())

	while 1:
		s = ser.read(1) 
		sys.stdout.write(s)
		sys.stdout.flush()
		token += s

		pos = token.find("arietta login:")
		if pos >= 0:
			token=""
			ser.write("root\r")
			continue

		pos = token.find("Password:")
		if pos >= 0:
			token=""
			ser.write("acmesystems\r")
			continue

		pos = token.find("Last login:")
		if pos >= 0:
			token=""
			time.sleep(0.5)
			ser.write("ifconfig wlan0\r")
			continue

finally:
	termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)





