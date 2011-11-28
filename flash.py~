#!/usr/bin/python

# flash.py 
# versione per la produzione di pizzica.py

# In Circuit Programming utility for FOX Board and Netus G20  
#
# Author: Sergio Tanzilli - tanzilli@acmesystems.it
#
# Copyright 2010 Acme Systems srl. Ladispoli (Rome) Italy
# http://www.acmesystems.it
# All Rights Reserved.
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import serial
import time
import sys
import getopt
import string 
from xmodem import XMODEM

filename = "acme_boot_1.20.bin"
serialdevice = "/dev/ttyUSB0"

print "Programmazione memorua flash su FOX Board G20"

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

print "Se la FOX contiene gia' un boot loader su memoria flash"
print "chiudi i contatti e riaccendi la FOX."

while True:
	ser.flushInput()
	ser.write("#")
	time.sleep(1)
	if ser.read(1)=='>':
	    break

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

print "--- Messaggi di boot in arrivo dalla FOX ---"

while True:
    s = ser.read(1) 
    sys.stdout.write(s)


ser.close()


