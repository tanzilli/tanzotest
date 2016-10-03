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

print "Banco di Test Multicon Gateway - ACME-0011"


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

		pos = token.find("aria login:")
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
			ser.write("echo 79 > /sys/class/gpio/export\r")
			ser.write("echo 80 > /sys/class/gpio/export\r")
			ser.write("echo 81 > /sys/class/gpio/export\r")
			ser.write("echo 82 > /sys/class/gpio/export\r")
			ser.write("echo 83 > /sys/class/gpio/export\r")
			ser.write("echo 84 > /sys/class/gpio/export\r")

			ser.write("echo 1 > /sys/class/gpio/export\r")
			ser.write("echo 6 > /sys/class/gpio/export\r")
			ser.write("echo 8 > /sys/class/gpio/export\r")

			ser.write("echo out > /sys/class/gpio/pioC15/direction\r")
			ser.write("echo out > /sys/class/gpio/pioC16/direction\r")
			ser.write("echo out > /sys/class/gpio/pioC17/direction\r")
			ser.write("echo out > /sys/class/gpio/pioC18/direction\r")
			ser.write("echo out > /sys/class/gpio/pioC19/direction\r")
			ser.write("echo out > /sys/class/gpio/pioC20/direction\r")

			ser.write("echo in > /sys/class/gpio/pioA1/direction\r")
			ser.write("echo in > /sys/class/gpio/pioA6/direction\r")
			ser.write("echo in > /sys/class/gpio/pioA8/direction\r")

			continue

		if isData():
			c = sys.stdin.read(1)
			if c == '\x1b':         # x1b is ESC
				print "\n"
				print color_pass + " Risultato finale dei test" + color_normal
				print "\n"
				ser.close()
				break
				
			if c == "w":
				ser.write("lsusb | grep Ralink\r")
				continue
				
			if c == "n":
				ser.write("ping -c 4 www.acmesystems.it\r")
				continue

			if c == "m":
				print "Rele 1 ON"
				ser.write("echo 1 > /sys/class/gpio/pioC15/value\r")
				time.sleep(1)
				
				print "Rele 2 ON"
				ser.write("echo 1 > /sys/class/gpio/pioC16/value\r")
				time.sleep(1)

				print "Rele 3 ON"
				ser.write("echo 1 > /sys/class/gpio/pioC17/value\r")
				time.sleep(1)

				print "Led rosso ON"
				ser.write("echo 1 > /sys/class/gpio/pioC18/value\r")
				time.sleep(1)w

				print "Led verde ON"
				ser.write("echo 1 > /sys/class/gpio/pioC19/value\r")
				time.sleep(1)

				print "Buzzer OFF"
				ser.write("echo 1 > /sys/class/gpio/pioC20/value\r")
				time.sleep(1)
				
				print "Rele 1 OFF"
				ser.write("echo 0 > /sys/class/gpio/pioC15/value\r")
				time.sleep(1)
				
				print "Rele 2 OFF"
				ser.write("echo 0 > /sys/class/gpio/pioC16/value\r")
				time.sleep(1)

				print "Rele 3 OFF"
				ser.write("echo 0 > /sys/class/gpio/pioC17/value\r")
				time.sleep(1)

				print "Led rosso OFF"
				ser.write("echo 0 > /sys/class/gpio/pioC18/value\r")
				time.sleep(1)

				print "Led verde OFF"
				ser.write("echo 0 > /sys/class/gpio/pioC19/value\r")
				time.sleep(1)

				print "Buzzer ON"
				ser.write("echo 0 > /sys/class/gpio/pioC20/value\r")
				time.sleep(1)

				continue

			if c == "s":
				print "Test seriale"
				ser.write("cat /sys/class/gpio/pioA1/value\r")
				ser.write("cat /sys/class/gpio/pioA6/value\r")
				ser.write("cat /sys/class/gpio/pioA8/value\r")
				time.sleep(1)

			if c == "h":
				ser.write("halt\r");
				continue

			if c == "rw":
				ser.write("reboot\r");
				continue


finally:
	termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)





