#!/usr/bin/python

import serial
import time
import sys
import getopt
import string 
from xmodem import XMODEM
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

############################################
#def test ():
#	token=""
#	while True:

############################################

#filename = "acmeboot_serialflash_1.20.bin"
filename = "acmeboot_dataflash_1.20.bin"
serialdevice = "/dev/ttyUSB0"

print "Programmazione memoria flash su FOX Board G20"

#If exist a file called macaddress.txt read and increment it
try:
	f = open("macaddress.txt",'r')
	b = f.read()
	c = "0x" + b[0:2] + b[3:5] + b[6:8] + b[9:11] + b[12:14] + b[15:17]
	d = int(c,16) +1
	a = ("%012X") % d
	b = a[0:2] + ":" + a[2:4]+ ":" + a[4:6] + ":" + a[6:8] + ":" + a[8:10] + ":" + a[10:12]
	f.close()

	f = open("macaddress.txt",'w')
	f.write(b + "\n")
	f.close()
except:
	print "macaddress.txt not found"

#Read the original executable file to send
f = open(filename,'rb')
buffer = f.read()
f.close()

#Search on it the MagicNumber to know where patch the Mac address
MacPosition=string.find(buffer, "\x5C\x5C\x5C\x5C") 

try:
	if MacPosition<>-1:
		MacPosition+=4
		macpatch = chr(int("0x" + a[0:2],16)) + chr(int("0x" + a[2:4],16)) + chr(int("0x" + a[4:6],16)) + chr(int("0x" + a[6:8],16)) + chr(int("0x" + a[8:10],16)) +  chr(int("0x" + a[10:12],16)) 
		patched_bin = buffer[:MacPosition] +  macpatch + buffer[MacPosition+6:]
		f = open(filename + "_patched",'wb')
		f.write(patched_bin)
		f.close()
except:
	print "Binary file not patched"

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

#Define the getc and putc function required from the
#xmodem module
def getc(size, timeout=1):
	data = ser.read(size)
	return data

def putc(data, timeout=1):
	ser.write(data)
	return len(data)

x = XMODEM(getc, putc)

print
print "Se la FOX contiene gia' un boot loader su memoria flash"
print "chiudi i contatti e riaccendi la FOX."
print

while True:
	ser.flushInput()
	ser.write("#")
	time.sleep(1)
	if ser.read(1)=='>':
	    break
###############
#	if ser.read(1)!= 'R':
#		test()
###############

ser.flushInput()

address=0x200000
cmdstring = "S%06X,#" % (address)
print "Send: [" + cmdstring + "]"
ser.write(cmdstring)


stream = open(filename + "_patched", 'rb')
x.send(stream)
stream.close()

while ser.read(1)!='>':
    pass

cmdstring = "G200000#"
print "Send: [" + cmdstring + "]"
ser.write(cmdstring)



print
print "--- Messaggi di boot in arrivo dalla FOX ---"
print

token=""
while True:
	s = ser.read(1) 
	sys.stdout.write(s)
	sys.stdout.flush()
	token += s

	pos = token.find("Linux version")
	if pos >= 0:
		token=""
		print "\n\nFlash terminato\n"
		break

	pos = token.find("No microSD")
	if pos >= 0:
		token=""
		print "Inserire la microSD per continuare"
		continue


print "\nSpegnere la Fox e premere Enter\n"

ser.flushInput()
ser.flushOutput()
# optional wait for keypress
raw_input('Press Enter...')

ser.flushInput()
ser.flushOutput()
print "\nRiaccendi la Fox\n"





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



ser.flushInput()
ser.flushOutput()

print "Caratteri in ricezione dalla DebugPort (type Ctrl-C to exit)"

s = ""
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

	pos = token.find("debarm login:")
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




