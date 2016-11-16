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
	print "a) Led ON"
	print "b) Led ON"
	print "c) Modem ON"
	print "d) Modem OFF"
	print "e) SIM 1"
	print "f) SIM 2"
	print "z) Open modems serial port"
	print "v) Send AT\n"
	print "x) Close modems serial port"
	print "--------------------------"
	print "h) Help"
	print "q) Exit"

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
			if c == '\x1b':         # x1b is ESC
				print "\n"
				print color_pass + " Risultato finale dei test" + color_normal
				print "\n"
				ser.close()
				break
				
			if c == "a":
				led_verde.on()
				led_sim1.on()
				led_sim2.on()
				continue

			if c == "b":
				led_verde.off()
				led_sim1.off()
				led_sim2.off()
				continue

			if c == "c":
				print "Modem ON"
				modem_power.on()
				continue

			if c == "d":
				print "Modem OFF"
				modem_power.off()
				continue
				
			if c == "e":
				print "SIM 1"
				sim_select.off()
				continue

			if c == "f":
				print "SIM 2"
				sim_select.on()
				continue

			if c == "z":
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

			if c == "v":
				print "Send AT\r"
				modem_serial_id.write("AT\r")

			if c == "x":
				print "Close modem serial port"
				modem_opened=False
				modem_serial_port.close()
  
#ser.flushInput()


			if c == "r":
				print "SIM 2"
				sim_select.on()
				continue

			if c == "2":
				ser.write("ping -c 4 www.acmesystems.it\r");
				continue

			if c == "h":
				menu()

			if c == "q":
				termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
				quit()

finally:
	termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
