#!/usr/bin/python
# Banco di Test per Aria G25
# Software lato Aria G25
# Authors: 
# 	Roberto Asquini - asquini@acmesystems.it
# 	Sergio Tanzilli - tanzilli@acmesystems.it

import time
import acmeboards
import serial
import sys
import os

#greenled PC20
#redled PC21

# Test GPIO

print "Test LEDs"
LEDR = acmeboards.Pin('N','23','low')
LEDG = acmeboards.Pin('N','22','high')
time.sleep(0.3)
LEDR = acmeboards.Pin('N','23','high')
LEDG = acmeboards.Pin('N','22','low')
time.sleep(0.3)
LEDR = acmeboards.Pin('N','23','low')
LEDG = acmeboards.Pin('N','22','high')
time.sleep(0.3)
LEDR = acmeboards.Pin('N','23','high')
LEDG = acmeboards.Pin('N','22','low')
time.sleep(0.3)
LEDR = acmeboards.Pin('N','23','low')
LEDG = acmeboards.Pin('N','22','low')


print "Test GPIO"


test = { 
	"N" : [
		["2","3"],
		["4","5"],
		["6","7"],
		["8","9"],
		["10","11"],
		["12","13"],
		["14","15"],
		["16","17"],
		["18","19"],
		["20","21"],
	],
	"E" : [
		["2","3"],
		["4","5"],
		["6","7"],
		["8","9"],
		["10","11"],
	],
	"S" : [
		["23","22"],
		["21","20"],
		["19","18"],
		["17","16"],
		["15","12"],
		["11","10"],
		["9","2"],
	],
	"W" : [
		["9","10"],
		["11","12"],
		["13","14"],
		["15","16"],
		["17","18"],
		["20","21"],
		["22","23"],
	],
}
while True:
	error_counter=0
	
	for connector_index, connector_item in enumerate(test):
		#print connector_index, connector_item, test[connector_item]

		for test_index, test_item in enumerate(test[connector_item]):
			#for pin_index, pin_item in enumerate(test[connector_item][test_index]):
			#print "Test %s.%s - %s.%s" % (connector_item,test_item[0],connector_item,test_item[1])
		
			#TEST A pin su anodo alto
			#  Il pin sul catodo deve valere 1

			pin_out = acmeboards.Pin(connector_item,test_item[0],'high')
			pin_in = acmeboards.Pin(connector_item,test_item[1],'in')

			if pin_in.get_value()<>1:
				print "TEST A: Pin %s.%s o %s.%s in corto verso massa" % (connector_item,test_item[0],connector_item,test_item[1])
				error_counter = error_counter + 1

			#TEST B pin su anodo basso
			#  Il pin sul catodo deve valere 1

			pin_out = acmeboards.Pin(connector_item,test_item[0],'low')
			pin_in = acmeboards.Pin(connector_item,test_item[1],'in')

			if pin_in.get_value()<>1:
				print "TEST B: Pin %s.%s e %s.%s in corto" % (connector_item,test_item[0],connector_item,test_item[1])
				error_counter = error_counter + 1

			#TEST C pin su catodo basso
			#  Il pin sul anodo deve valere 0

			pin_in = acmeboards.Pin(connector_item,test_item[0],'in')
			pin_out = acmeboards.Pin(connector_item,test_item[1],'low')
			
			if pin_in.get_value()<>0:
				print "TEST C: Pin %s.%s o %s.%s staccati" % (connector_item,test_item[0],connector_item,test_item[1])
				error_counter = error_counter + 1

			#TEST D pin su catodo alto
			#  Il pin sul anodo deve valere 1

			pin_in = acmeboards.Pin(connector_item,test_item[0],'in')
			pin_out = acmeboards.Pin(connector_item,test_item[1],'high')

			if pin_in.get_value()<>1:
				print "TEST D: Pin %s.%s o %s.%s in corto verso massa" % (connector_item,test_item[0],connector_item,test_item[1])
				error_counter = error_counter + 1
			# ripristina il pin di uscita in ingresso
			pin_out = acmeboards.Pin(connector_item,test_item[1],'in')

	if error_counter==0:
		break
	else:
		LEDR = acmeboards.Pin('N','23','high')
		LEDG = acmeboards.Pin('N','22','low')
		time.sleep(1)

print "GPIO test OK"

os.system("rm index.html");

if os.system("wget http://192.168.1.1")==0:
	print "ETH test OK"
else:
	print "Errore di rete"


os.system("umount /dev/sda1");
os.system("umount /dev/sdb1");
os.system("umount /dev/sdc1");

if os.system("mount -t vfat /dev/sda1 /mnt/usbkey1")==0:
	print "1) USB test OK"
else:
	print "1) Errore USB"


if os.system("mount -t vfat /dev/sdb1 /mnt/usbkey2")==0:
	print "2) USB test OK"
else:
	print "2) Errore USB"


if os.system("mount -t vfat /dev/sdc1 /mnt/usbkey3")==0:
	print "3) USB test OK"
else:
	print "3) Errore USB"

LEDR = acmeboards.Pin('N','23','low')
LEDG = acmeboards.Pin('N','22','high')
#os.system("halt");



