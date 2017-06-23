#!/usr/bin/python

# Banco di Test per NetusG20 e FOX Board G20
# Software lato PC
# Author: Sergio Tanzilli - tanzilli@acmesystems.it

import serial
import time
import sys
import getopt
import string 
import datetime

color_warning = "\x1B[30;41m" 
color_pass = "\x1B[30;42m" 
color_normal = "\x1B[0m" 

elenco_test = {
	"AcmeBoot":"-",
	"microSD":"-",
	"sda1":"-",
	"sdb1":"-",
	"eth0":"-",
	"login":"-",
	"password":"-",
	"gpio":"-",
}


serialdevice = "/dev/ttyUSB0"

print "Banco di Test NetusG20"
print "Version: 2.01"


#Open the serial port 
ser = serial.Serial(
	port=serialdevice, 
	baudrate=115200, 
	timeout=1,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS
)  
ser.flushInput()

print "Caratteri in ricezione dalla DebugPort (type Ctrl-C to exit)"

token=""
while True:
	s = ser.read(1) 
	sys.stdout.write(s)
	sys.stdout.flush()
	token += s

	pos = token.find("AcmeBoot")
	if pos >= 0:
		token=""
		elenco_test["AcmeBoot"]="OK"
		continue
 
	pos = token.find("Jump to Kernel")
	if pos >= 0:
		token=""
		elenco_test["microSD"]="OK"
		continue

	pos = token.find("sda1")
	if pos >= 0:
		token=""
		elenco_test["sda1"]="OK"
		continue

	pos = token.find("sdb1")
	if pos >= 0:
		token=""
		elenco_test["sdb1"]="OK"
		continue

	pos = token.find("netusg20 login:")
	if pos >= 0:
		token=""
		elenco_test["login"]="OK"
		ser.write("root\r")
		continue

	pos = token.find("Password:")
	if pos >= 0:
		token=""
		elenco_test["password"]="OK"
		ser.write("netusg20\r")
		time.sleep(0.5)
		ser.write("./gpio.py\r")
		continue

	pos = token.find("GPIO test OK")
	if pos >= 0:
		token=""
		dataoracorrente=datetime.datetime.now().strftime("%m%d%H%M%Y")
		comando =  "date " + dataoracorrente + "\r"
		ser.write(comando)

		elenco_test["gpio"]="OK"
		continue

	pos = token.find("`index.html' saved")
	if pos >= 0:
		token=""

		ser.write("halt\r")

		elenco_test["eth0"]="OK"
		continue

	pos = token.find("Power down")
	if pos >= 0:
		token=""
		break

print "\n"
print color_pass + " Risultato finale dei test" + color_normal
print "\n"

for test in elenco_test:
	print test + " -> ",

	if elenco_test[test]=="OK":
		print elenco_test[test]
	else:
		print color_warning + "error" + color_normal

ser.close()


