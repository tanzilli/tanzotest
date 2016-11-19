#!/usr/bin/python

# Banco di Test per ACME-0001 FoxBox mini

from acmepins import GPIO
from time import sleep

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

tasto = GPIO('PC12','INPUT') 
led_verde = GPIO('PC8','LOW') 
led_sim1  = GPIO('PC14','LOW') 
led_sim2  = GPIO('PC16','LOW') 
modem_power  = GPIO('PC13','LOW') 
sim_select  = GPIO('PA4','LOW') 

def menu():
	print "Test ACME-0001 FoxBox mini"
	print "--------------------------"
	print "q) Leds ON"
	print "w) Leds OFF"
	print "a) Modem ON"
	print "s) Modem OFF"
	print "z) SIM 1"
	print "x) SIM 2"
	print "1) Open modems serial port"
	print "2) Send AT"
	print "p) ping www.acmesystems.it"
	print "--------------------------"
	print "h) Help"
	print "ESC) Exit"

def isData():
	return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

color_warning = "\x1B[30;41m" 
color_pass = "\x1B[30;42m" 
color_normal = "\x1B[0m" 

old_settings = termios.tcgetattr(sys.stdin)

modem_opened=False

print "Caratteri in ricezione dalla DebugPort (type Ctrl-C to exit)"
menu()

token=""

try:
	tty.setcbreak(sys.stdin.fileno())

	while 1:
		if tasto.get_value()==0:
			print "Tasto premuto"

		if modem_opened==True:
			s = modem_serial_id.read(1) 
			sys.stdout.write(s)
			sys.stdout.flush()
			token += s

			pos = token.find("acqua login:")
			if pos >= 0:
				token=""
				modem_serial_id.write("root\r")
				continue

				pos = token.find("Password:")
				if pos >= 0:
					token=""
					modem_serial_id.write("acmesystems\r")
					continue

		if isData():
			c = sys.stdin.read(1)
				
			if c == "q":
				print "Leds ON"
				led_verde.on()
				led_sim1.on()
				led_sim2.on()
				continue

			if c == "w":
				print "Leds OFF"
				led_verde.off()
				led_sim1.off()
				led_sim2.off()
				continue

			if c == "a":
				print "Modem ON"
				modem_power.on()
				continue

			if c == "s":
				print "Modem OFF"
				modem_power.off()
				continue
				
			if c == "z":
				print "SIM 1"
				sim_select.off()
				continue

			if c == "x":
				print "SIM 2"
				sim_select.on()
				continue

			if c == "1":
				print "Open modem serial port"
				modem_serial_id = serial.Serial(
					port="/dev/ttyUSB0", 
					baudrate=115200, 
					timeout=0.1,
					parity=serial.PARITY_NONE,
					stopbits=serial.STOPBITS_ONE,
					bytesize=serial.EIGHTBITS
				)
				modem_opened=True
				continue

			if c == "2":
				print "Send AT\r"
				modem_serial_id.write("AT\r")

			if c == '\x1b':         # x1b is ESC
				print "Close modem serial port"
				modem_opened=False
				modem_serial_port.close()
				termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
				quit()
  
			if c == "p":
				ser.write("ping -c 4 www.acmesystems.it\r");
				continue

			if c == "h":
				menu()

finally:
	termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
