#!/usr/bin/python
# Banco di Test per Acqua su banco ad aghi definitivo
# Software lato Acqua
#
# Authors: 
# 	Roberto Asquini - asquini@acmesystems.it
# 	Sergio Tanzilli - tanzilli@acmesystems.it

import time
import acmepins
import sys
import os
import subprocess

color_warning = "\x1B[30;41m"
color_pass = "\x1B[30;42m"
color_normal = "\x1B[0m"
color_check = "\x1B[31m" 

numerrors = 0
step = 0  

testlistpullup = [ 
	["PA0","PA1"],
	["PA2","PA3"],
	["PA4","PA5"],
	["PA6","PA7"],
	["PA8","PA9"],
	["PA10","PA11"],
	["PA12","PA13"],
	["PA14","PA15"],
	["PC14","PC13"],
	["PC12","PC11"],
	["PC10","PC15"],
	["PE27","PE28"],
	["PA28","PA27"],
	["PA26","PA29"],
	["PD20","PA24"],
	["PD22","PD21"],
	["PD24","PD23"],
	["PD26","PD25"],
	["PD28","PD27"],
	["PD29","PA25"],
	["PD19","PB10"],
	["PD12","PD13"],
	["PD10","PD11"],
	["PD14","PD15"],
	["PD16","PD17"],
	["PD18","PB2"],
	["PB3","PB6"],
	["PB11","PB7"],
	["PB4","PB5"],
	["PB14","PB1"],
	["PB15","PB8"],
	["PB16","PB9"],
	["PB17","PB12"],
	["PB18","PB13"],
	["PB27","PB0"],
	["PB25","PB26"],
	["PB29","PB28"],
	["PB23","PB22"],
	["PB21","PB19"],
	["PB20","PB24"],
	["PC23","PC27"],
	["PC22","PC25"],
	["PC26","PC24"],
	["PC30","PC28"],
	["PC31","PC29"],
	["PA16","PA17"],
	["PA18","PA19"],
	["PA20","PA21"],
	["PA22","PA23"],
	["PA30","PA31"],
	["PE29","PE31"],
	["PC17","PC16"],
	["PC19","PC18"],
	["PC21","PC20"],
]

testlistpulldown = [ 
	["PE16","PE17"],
	["PE18","PE19"],
	["PE23","PE15"],
	["PE25","PE24"],
]

testlistPE20PE26 = [ 
	["PE20","PE26"],
]

time.sleep(0.1)
#***********************************************************************
# Test RAM
#***********************************************************************

print "Test RAM"


print "DDR2 RAM Test"
if os.system("memtester 20k 1")==0:
	print color_pass + "Memory OK" + color_normal
else:
	print color_warning + "Memory ERROR !" + color_normal
	numerrors = numerrors + 1

print ""

#***********************************************************************
# Test Ethernet
#***********************************************************************

print "Test Ethernet"


#os.system("rm index.html");
if os.system("ping -c 2 192.168.1.101")==0:
	print color_pass + "ETH test OK" + color_normal
	error_eth = 0
else:
	print color_warning + "ERRORE DI RETE" + color_normal
	numerrors = numerrors+1
	error_eth = 1

print ""

#***********************************************************************
# Test GPIO
#***********************************************************************

print "Test GPIO"

# Ciclo di scansione e test dei GPIO

error_counter=0

for test in testlistPE20PE26:
	acmepins.setup(test[0],acmepins.OUT,0)
	acmepins.setup(test[1],acmepins.IN,0)
	if step == 1:
		print "%s -> %s" % (test[0],test[1])
		print "test0=1" 
	acmepins.output(test[0],1)
	if step == 1:
		raw_input("Press Enter")
	if acmepins.input(test[1])==0:
		print (color_warning + "%s=1 --> %s==1 ?" + color_normal) % (test[0],test[1]),
		print (color_warning + "Errore ! %s in corto verso massa oppure %s o %s a circuito aperto" + color_normal) % (test[1])
		error_counter = error_counter + 1
		if step == 1:
			raw_input(" Press Enter")
	acmepins.output(test[0],0)
	if step == 1:
		print "test0=0"
		raw_input("Press Enter")
	if acmepins.input(test[1])==1:
		print (color_warning + "%s=0 --> %s==0 ? " + color_normal) % (test[0],test[1]),
		print (color_warning + "Errore ! %s in corto verso 3V3 oppure %s o %s a circuito aperto" + color_normal) % (test[1], test[0], test[1])
		error_counter = error_counter + 1
		if step == 1:
			raw_input("  Press Enter")
	acmepins.setup(test[0],acmepins.IN,0)
	acmepins.setup(test[1],acmepins.OUT,0)

	acmepins.output(test[1],1)
	if step == 1:
		print "test1=1"
		raw_input("Press Enter")
	if acmepins.input(test[0])==0:
		print (color_warning + "%s==1 ? <-- %s=1" + color_normal) % (test[0],test[1]),
		print (color_warning + "Errore ! %s in corto verso massa oppure %s o %s a circuito aperto" + color_normal) % (test[0], test[0], test[1])
		error_counter = error_counter + 1
		if step == 1:
			raw_input("   Press Enter")

	acmepins.output(test[1],0)
	if step == 1:
		print "test1=0"
		raw_input("Press Enter")
	if acmepins.input(test[0])==1:
		print color_warning + "%s==0 ? <-- %s=0 " % (test[0],test[1]),
		print color_warning + "Errore ! %s a 3.3v" % (test[0])
		error_counter = error_counter + 1
		if step == 1:
			raw_input("    Press Enter")

	acmepins.setup(test[0], acmepins.IN,0)
	acmepins.setup(test[1], acmepins.IN,0)

if error_counter==0:
	print color_pass + "GPIO test PE20PE26 OK" + color_normal
else:
	print (color_warning + "Errors pullupdown: %d" + color_normal) % error_counter
	numerrors = numerrors + 1

time.sleep(0.01)

error_counter = 0
for test in testlistpullup:
	acmepins.setup(test[0],acmepins.OUT,0)
	acmepins.setup(test[1],acmepins.IN,0)
	if step == 1:
		print "%s -> %s" % (test[0],test[1])
		print "test0=1" 
	acmepins.output(test[0],1)
	if step == 1:
		raw_input("Press Enter")
	if acmepins.input(test[1])==0:
		print (color_warning + "%s=1 --> %s==1 ?" + color_normal) % (test[0],test[1]),
		print (color_warning + "Errore ! %s in corto verso massa" + color_normal) % (test[1])
		error_counter = error_counter + 1
		if step == 1:
			raw_input(" Press Enter")

	acmepins.output(test[0],0)
	if step == 1:
		print "test0=0"
		raw_input("Press Enter")
	if acmepins.input(test[1])==0:
		print (color_warning + "%s=0 --> %s==1 ? " + color_normal) % (test[0],test[1]),
		print (color_warning + "Errore ! Corto tra %s e %s" + color_normal) % (test[0],test[1])
		error_counter = error_counter + 1
		if step == 1:
			raw_input(" Press Enter")

	acmepins.setup(test[0],acmepins.IN,0)
	acmepins.setup(test[1],acmepins.OUT,0)

	acmepins.output(test[1],1)
	if step == 1:
		print "test1=1"
		raw_input("Press Enter")
	if acmepins.input(test[0])==0:
		print (color_warning + "%s==1 ? <-- %s=1" + color_normal) % (test[0],test[1]),
		print (color_warning + "Error ! %s in corto verso massa" + color_normal) % (test[0])
		error_counter = error_counter + 1
		if step == 1:
			raw_input(" Press Enter")

	acmepins.output(test[1],0)
	if step == 1:
		print "test1=0"
		raw_input("Press Enter")
	if acmepins.input(test[0])==1:
		print (color_warning + "%s==0 ? <-- %s=0 " + color_normal) % (test[0],test[1]),
		print (color_warning + "Errore ! %s o %s a circuito aperto oppure %s a 3.3v" + color_normal) % (test[0],test[1],test[0])
		error_counter = error_counter + 1
		if step == 1:
			raw_input(" Press Enter")

	acmepins.setup(test[0], acmepins.IN,0)
	acmepins.setup(test[1], acmepins.IN,0)

if error_counter==0:
	print color_pass + "GPIO pullup test OK" + color_normal
else:
	print (color_warning + "Errors pullup: %d" + color_normal) % error_counter
	numerrors = numerrors + 1

time.sleep(0.1)

error_counter = 0
for test in testlistpulldown:
	acmepins.setup(test[0],acmepins.OUT,0)
	acmepins.setup(test[1],acmepins.IN,0)
	if step == 1:
		print "%s -> %s" % (test[0],test[1])
		print "test0=1" 
	acmepins.output(test[0],1)
	if step == 1:
		raw_input("Press Enter")
	if acmepins.input(test[1])==0:
		print (color_warning + "%s=1 --> %s==1 ?" + color_normal) % (test[0],test[1]),
		print (color_warning + "Errore ! %s o %s a circuito aperto" + color_normal) % (test[0], test[1])
		error_counter = error_counter + 1
		if step == 1:
			raw_input(" Press Enter")

	acmepins.output(test[0],0)
	if step == 1:
		print "test0=0"
		raw_input("Press Enter")
	if acmepins.input(test[1])==1:
		print (color_warning + "%s=0 --> %s==0 ? " + color_normal) % (test[0],test[1]),
		print (color_warning + "Errore ! %s in corto verso 3V3" + color_normal) % (test[1])
		error_counter = error_counter + 1
		if step == 1:
			raw_input(" Press Enter")

	acmepins.setup(test[0],acmepins.IN,0)
	acmepins.setup(test[1],acmepins.OUT,0)

	acmepins.output(test[1],1)
	if step == 1:
		print "test1=1"
		raw_input("Press Enter")
	if acmepins.input(test[0])==1:
		print (color_warning + "%s==0 ? <-- %s=1" + color_normal) % (test[0],test[1]),
		print (color_warning + "Errore ! %s e %s in corto tra loro" + color_normal) % (test[0])
		error_counter = error_counter + 1
		if step == 1:
			raw_input(" Press Enter")

	acmepins.output(test[1],0)
	if step == 1:
		print "test1=0"
		raw_input("Press Enter")
	if acmepins.input(test[0])==1:
		print (color_warning + "%s==0 ? <-- %s=0 " + color_normal) % (test[0],test[1]),
		print (color_warning + "Errore ! %s a 3.3v" + color_normal) % (test[0])
		error_counter = error_counter + 1
		if step == 1:
			raw_input(" Press Enter")

	acmepins.setup(test[0], acmepins.IN,0)
	acmepins.setup(test[1], acmepins.IN,0)

if error_counter==0:
	print color_pass + "GPIO pulldown test OK" + color_normal
else:
	print (color_warning + "Errors pulldown: %d" + color_normal) % error_counter
	numerrors = numerrors + 1

time.sleep(0.1)


print ""

#***********************************************************************
# Test USB
#***********************************************************************
'''
print "Test USB"

#os.system("umount /dev/sda1");
#os.system("umount /dev/sdb1");
#os.system("umount /dev/sdc1");

if os.system("mount -t vfat /dev/sda1 /mnt/usbkey1")==0:
	print color_pass + "1) USB test OK" + color_normal
else:
	print color_warning + "1) Errore USB" + color_normal
	numerrors = numerrors + 1

if os.system("mount -t vfat /dev/sdb1 /mnt/usbkey2")==0:
	print color_pass + "2) USB test OK" + color_normal
else:
	print color_warning + "2) Errore USB" + color_normal
	numerrors = numerrors + 1

if os.system("mount -t vfat /dev/sdc1 /mnt/usbkey3")==0:
	print color_pass + "3) USB test OK" + color_normal
else:
	print color_warning + "3) Errore USB" + color_normal
	numerrors = numerrors + 1
time.sleep(2)
os.system("umount /dev/sda1");
os.system("umount /dev/sdb1");
os.system("umount /dev/sdc1");


print ""
'''

#***********************************************************************        
# Test A/D Converter and 3V3ETH
#***********************************************************************        
print "Test USB with DPIs"

if os.system("ls /dev/ttyUSB0")==0:
	print color_pass + "1) USB test OK" + color_normal
else:
	print color_warning + "1) Errore USB" + color_normal
	numerrors = numerrors + 1

if os.system("ls /dev/ttyUSB1")==0:
	print color_pass + "2) USB test OK" + color_normal
else:
	print color_warning + "2) Errore USB" + color_normal
	numerrors = numerrors + 1

if os.system("ls /dev/ttyUSB2")==0:
	print color_pass + "3) USB test OK" + color_normal
else:
	print color_warning + "3) Errore USB" + color_normal
	numerrors = numerrors + 1

#***********************************************************************        
# Test A/D Converter and 3V3ETH
#***********************************************************************        

print "Test A/D and 3V3ETH"

error_counter = 0
#acmepins.setup("PE12",acmepins.OUT,0)
#print "3V3ETH ON"
#print "test AD10"
os.system("cp /sys/bus/iio/devices/iio\:device0/in_voltage10_raw ad10")
ad10 = subprocess.check_output(["cat", "ad10"])
test = [int(s) for s in ad10.split() if s.isdigit()][0]  #estrae il numero
print "ad10 = %d" % (test)
if test<3200 or test>3900:
	print (color_warning + "Error AD10! %s (3200..3900)" + color_normal) % (test)
	error_counter = error_counter+1 
	numerrors = numerrors+1
#print "test AD11"
os.system("cp /sys/bus/iio/devices/iio\:device0/in_voltage11_raw ad11")
ad11 = subprocess.check_output(["cat", "ad11"])
test = [int(s) for s in ad11.split() if s.isdigit()][0]  #estrae il numero
print "ad11 = %d" % (test)
if test<1500 or test>2200:
	print (color_warning + "Error AD11! %s (1500..2200)" + color_normal) % (test)
	error_counter = error_counter+1 
	numerrors = numerrors+1

''' 
acmepins.output("PE12",1)
print "3V3ETH OFF"
raw_input("Press Enter")
print "test AD10"
print "%s" % (os.system("cat /sys/bus/iio/devices/iio\:device0/in_voltage10_raw"))
print "test AD11"
print "%s" % (os.system("cat /sys/bus/iio/devices/iio\:device0/in_voltage11_raw"))

'''

if error_counter==0:
	print color_pass + "AD converter test OK" + color_normal
else:
	print (color_warning + "AD converter Errors: %d" + color_normal) % error_counter
	time.sleep(1)

# ripete errore di rete per chiarezza
if error_eth==0:
	print color_pass + "ETH test OK" + color_normal
else:
	print color_warning + "ERRORE DI RETE" + color_normal


if numerrors ==0:
	print color_pass + "numerrors = %d " % numerrors
	print color_pass + " TEST OK. YOU CAN SWITCH OFF !" + color_normal
#	os.system("halt");
else:
	print color_warning + "numerrors = %d " % numerrors




	print color_warning + " ERRORS !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" + color_normal

os.system("halt")
