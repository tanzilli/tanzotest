#!/usr/bin/python

# Banco di Test per Multicon Touch
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

print "Banco di Test Multicon Touch"


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

		pos = token.find("acqua login:")
		if pos >= 0:
			token=""
			ser.write("root\r")
			continue

		pos = token.find("Password:")
		if pos >= 0:
			token=""
			ser.write("acmesystems\r")
			continue

		if isData():
			c = sys.stdin.read(1)
			if c == '\x1b':         # x1b is ESC
				print "\n"
				print color_pass + " Risultato finale dei test" + color_normal
				print "\n"
				ser.close()
				break
				
			if c == "1":
				ser.write("DISPLAY=\":0\" xinput_calibrator --geometry 480x272\r");
				continue
				
			if c == "2":
				ser.write("ping -c 4 www.acmesystems.it\r");
				continue

			if c == "h":
				ser.write("halt\r");
				continue

finally:
	termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)





