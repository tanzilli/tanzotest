#!/usr/bin/python

import time
import fox
import serial
import sys
import os

# Test GPIO

testPhrase = "Test phrase"
color_warning = "\x1B[30;41m" 
color_normal = "\x1B[0m" 


ttyS1 = serial.Serial(
	port='/dev/ttyS1', 
	baudrate=115200, 
	timeout=1,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS
)  

ttyS2 = serial.Serial(
	port='/dev/ttyS2', 
	baudrate=115200, 
	timeout=1,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS
)  

ttyS3 = serial.Serial(
	port='/dev/ttyS3', 
	baudrate=115200, 
	timeout=1,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS
)  

ttyS4 = serial.Serial(
	port='/dev/ttyS4', 
	baudrate=115200, 
	timeout=1,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS
)  

ttyS5 = serial.Serial(
	port='/dev/ttyS5', 
	baudrate=115200, 
	timeout=1,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS
)  

ttyS6 = serial.Serial(
	port='/dev/ttyS6', 
	baudrate=115200, 
	timeout=1,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS
)  


print "----------> Inserisci J7 <-------------"

outLineJ7=[]
inpLineJ7=[]

outLineJ7.append('J7.3')
inpLineJ7.append('J7.4')

#outLineJ7.append('J7.5')
#inpLineJ7.append('J7.6')

outLineJ7.append('J7.7')
inpLineJ7.append('J7.8')

outLineJ7.append('J7.9')
inpLineJ7.append('J7.10')

outLineJ7.append('J7.11')
inpLineJ7.append('J7.12')

outLineJ7.append('J7.13')
inpLineJ7.append('J7.14')

outLineJ7.append('J7.35')
inpLineJ7.append('J7.36')

outLineJ7.append('J7.37')
inpLineJ7.append('J7.38')

for i in range (0,len(outLineJ7)):
	print "Line " + outLineJ7[i] + " on " + inpLineJ7[i]
	testOut = fox.Pin(outLineJ7[i],'low')
	testInp = fox.Pin(inpLineJ7[i],'in')

	print "Low"
	while True:
		testOut.setValue(0)
		if testInp.getValue()==0:
			break

	print "High"
	while True:
		testOut.setValue(1)
		if testInp.getValue()==1:
			break


#J7.34 DTR ttyS1
#J7.32 DSR ttyS1
#J7.33 RI ttyS1
#J7.31 CD ttyS1

print "J7.34 --> J7.31-32-33"
print "Low"

while True:
	ttyS1.setDTR(False)
	if not ttyS1.getDSR():
		break

	if not ttyS1.getRI():
		break
	
	if not ttyS1.getCD():
		break
	
print "High"

while True:
	ttyS1.setDTR(True)
	if ttyS1.getDSR():
		break
	if ttyS1.getRI():
		break
	if ttyS1.getCD():
		break

#J7.22 TX ttyS3
#J7.21 RX ttyS3

print "Test /dev/ttyS3 (J7.22 -> J7.21)"
while True:
	ttyS3.flushInput()
	ttyS3.write(testPhrase)
	s = ttyS3.read(11)
	if (s==testPhrase):
		break
	time.sleep(1)

#Test del led (J7.17) letto su J7.15
print "Test LED (J7.17) --> J7.15"
j7_15 = fox.Pin('J7.15','in')

while j7_15.getValue():
	pass
while not j7_15.getValue():
	pass
while j7_15.getValue():
	pass
while not j7_15.getValue():
	pass	

print "----------> Inserisci J6 <-------------"

outLineJ6=[]
inpLineJ6=[]

outLineJ6.append('J6.17')
inpLineJ6.append('J6.18')

outLineJ6.append('J6.19')
inpLineJ6.append('J6.20')

outLineJ6.append('J6.25')
inpLineJ6.append('J6.26')

outLineJ6.append('J6.27')
inpLineJ6.append('J6.28')

outLineJ6.append('J6.29')
inpLineJ6.append('J6.30')

outLineJ6.append('J6.37')
inpLineJ6.append('J6.38')

inpLineJ6.append('J6.24')
inpLineJ6.append('J6.36')

for i in range (0,len(outLineJ6)):
	print "Line " + outLineJ6[i] + " on " + inpLineJ6[i]
	testOut = fox.Pin(outLineJ6[i],'low')
	testInp = fox.Pin(inpLineJ6[i],'in')

	print "Low"
	while True:
		testOut.setValue(0)
		if testInp.getValue()==0:
			break

	print "High"
	while True:
		testOut.setValue(1)
		if testInp.getValue()==1:
			break

#J6.9 TX ttyS1
#J6.8 RX ttyS1
print "Test /dev/ttyS1 (J6.9 -> J6.8)"
while True:
	ttyS1.flushInput()
	ttyS1.write(testPhrase)
	s = ttyS1.read(11)
	if (s==testPhrase):
		break
	time.sleep(1)

#J6.7 RTS ttyS1
#J6.10 CTS ttyS1
print "Test RTS --> CTS ttyS1 (J6.7 -> J6.10)"
print "Low"
while True:
	ttyS1.setRTS(False)
	if not ttyS1.getCTS():
		break
print "High"
while True:
	ttyS1.setRTS(True)
	if ttyS1.getCTS():
		break

#J6.5 TX ttyS2
#J6.4 RX ttyS2
print "Test /dev/ttyS2 (J6.5 -> J6.4)"
while True:
	ttyS2.flushInput()
	ttyS2.write(testPhrase)
	s = ttyS2.read(11)
	if (s==testPhrase):
		break
	time.sleep(1)

#J6.3 RTS ttyS2
#J6.6 CTS ttyS2
print "Test RTS --> CTS ttyS2 (J6.3 -> J6.6)"
print "Low"
while True:
	ttyS2.setRTS(False)
	if not ttyS2.getCTS():
		break
print "High"
while True:
	ttyS2.setRTS(True)
	if ttyS2.getCTS():
		break

#J6.14 TX ttyS4
#J6.13 RX ttyS4
print "Test /dev/ttyS4 (J6.14 -> J6.13)"
while True:
	ttyS4.flushInput()
	ttyS4.write(testPhrase)
	s = ttyS4.read(11)
	if (s==testPhrase):
		break
	time.sleep(1)

#J7.18 RTS ttyS4 Non utilizzabile perche definito come A5 

#J7.15 General I/O
#J7.16 CTS ttyS4

#j7_15 = fox.Pin('J7.15','low')
#if ttyS4.getCTS():
#	print "Error 0 to 1 : J7.15 --> J7.16"
	
#j7_15.setValue(1)
#if not ttyS4.getCTS():
#	print "Error 1 to 0 : J7.15 --> J7.16"



#J6.21 TX ttyS5
#J6.22 RX ttyS5
print "Test /dev/ttyS5 (J6.21 -> J6.22)"
while True:
	ttyS5.flushInput()
	ttyS5.write(testPhrase)
	s = ttyS5.read(11)
	if (s==testPhrase):
		break
	time.sleep(1)

#J6.16 TX ttyS6
#J6.15 RX ttyS6
print "Test /dev/ttyS6 (J6.16 -> J6.15)"
while True:
	ttyS6.flushInput()
	ttyS6.write(testPhrase)
	s = ttyS6.read(11)
	if (s==testPhrase):
		break
	time.sleep(1)

#Test del pulsante
#Uso J7.15 solo come appoggio per clearmi una istanza
#pulsante = fox.Pin('J7.15','in')
#pulsante.export(100)
#pulsante.direction('in')
#print "Premi il pulsante"
#while pulsante.getValue():
#	pass

ttyS1.close()
ttyS2.close()
ttyS3.close()
ttyS4.close()
ttyS5.close()
ttyS6.close()

print "[[TEST J6 J7 OK]]"

os.system("rm index.html");
os.system("wget http://www.acmesystems.it");




