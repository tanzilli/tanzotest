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


color_warning = "\x1B[30;41m"
color_pass = "\x1B[30;42m"
color_normal = "\x1B[0m"
color_check = "\x1B[31m" 

numerrors = 0

#***********************************************************************
# Test RAM
#***********************************************************************
'''
print "DDR2 RAM Test"
if os.system("memtester 50K 1")==0:
	print color_pass + "Memory OK" + color_normal
else:
	print color_warning + "Memory ERROR !" + color_normal
	numerrors = numerrors + 1
'''

#***********************************************************************
# Test Ethernet
#***********************************************************************

'''
os.system("rm index.html");
if os.system("wget http://192.168.1.1")==0:
	print color_pass + "ETH test OK" + color_normal
	error_eth = 0
else:
	print color_warning + "ERRORE DI RETE" + color_normal
	numerrors = numerrors+1
	error_eth = 1
'''

#***********************************************************************
# Test GPIO
#***********************************************************************

print "Test GPIO"

testlist = [ 
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
]

# Ciclo di scansione e test dei GPIO

error_counter=0

for test in testlist:
	acmepins.setup(test[0],acmepins.OUT,0)
	acmepins.setup(test[1],acmepins.IN,0)

	acmepins.output(test[0],1)
	print "%s=1 --> %s==1 ?" % (test[0],test[1])
	if acmepins.input(test[1])==0:
		print "Error !"
		error_counter = error_counter + 1

	print "%s=0 --> %s==1 ? " % (test[0],test[1])
	acmepins.output(test[0],0)
	if acmepins.input(test[1])==0:
		print "Error !"
		error_counter = error_counter + 1

	acmepins.setup(test[0],acmepins.IN,0)
	acmepins.setup(test[1],acmepins.OUT,0)

	acmepins.output(test[1],1)
	print "%s==1 ? <-- %s=1" % (test[0],test[1])
	if acmepins.input(test[0])==0:
		print "Error !"
		error_counter = error_counter + 1

	print "%s==0 ? --> %s=0 " % (test[0],test[1])
	acmepins.output(test[1],0)
	if acmepins.input(test[0])==1:
		print "Error !"
		error_counter = error_counter + 1

if error_counter==0:
	print color_pass + "GPIO test OK" + color_normal
else:
	print "Errors: %d" % error_counter
	time.sleep(1)


#***********************************************************************
# Test USB
#***********************************************************************

'''
os.system("umount /dev/sda1");
os.system("umount /dev/sdb1");
os.system("umount /dev/sdc1");

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
# ripete errore di rete per chiarezza
if error_eth==0:
	print color_pass + "ETH test OK" + color_normal
else:
	print color_warning + "ERRORE DI RETE" + color_normal
	numerrors = numerrors+1

if numerrors ==0:
	print color_pass + "numerrors = %d " % numerrors
	LEDR = ablib.Pin('N23','LOW')
	LEDG = ablib.Pin('N22','HIGH')
	print color_pass + " TEST OK. YOU CAN SWITCH OFF !" + color_normal
#	os.system("halt");
else:
	print color_warning + "numerrors = %d " % numerrors
	LEDR = ablib.Pin('N23','HIGH')
	LEDG = ablib.Pin('N22','LOW')
	print color_warning + " ERRORS !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" + color_normal
'''




