#!/usr/bin/python
# Banco di Test per Aria G25 rel 1.1
# Software lato Aria G25
# Authors: 
# 	Roberto Asquini - asquini@acmesystems.it
# 	Sergio Tanzilli - tanzilli@acmesystems.it

import time
import ablib
import serial
import sys
import os

#greenled PC20
#redled PC21

# Test GPIO

color_warning = "\x1B[30;41m"
color_pass = "\x1B[30;42m"
color_normal = "\x1B[0m"
color_check = "\x1B[31m" 

numerrors = 0

print "Test LEDs"
LEDR = ablib.Pin('N23','LOW')
LEDG = ablib.Pin('N22','HIGH')
time.sleep(0.1)
LEDR = ablib.Pin('N23','HIGH')
LEDG = ablib.Pin('N22','LOW')
time.sleep(0.1)
LEDR = ablib.Pin('N23','LOW')
LEDG = ablib.Pin('N22','HIGH')
time.sleep(0.1)
LEDR = ablib.Pin('N23','HIGH')
LEDG = ablib.Pin('N22','LOW')
time.sleep(0.1)
LEDR = ablib.Pin('N23','LOW')
LEDG = ablib.Pin('N22','LOW')

print "DDR2 RAM Test"
if os.system("memtester 50K 1")==0:
	print color_pass + "Memory OK" + color_normal
else:
	print color_warning + "Memory ERROR !" + color_normal
	numerrors = numerrors + 1

os.system("rm index.html");
if os.system("wget http://192.168.1.1")==0:
	print color_pass + "ETH test OK" + color_normal
	error_eth = 0
else:
	print color_warning + "ERRORE DI RETE" + color_normal
	numerrors = numerrors+1
	error_eth = 1

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
pin_open = ablib.Pin('N20','INPUT')
pin_test = ablib.Pin('N21','INPUT')
print "if N21 is LOW do not test GPIOs"
time.sleep(0.1)
if pin_test.get_value()<>0:
	print "Test N21 (PC19) is HIGH"
	while True:
		error_counter=0
	
		for connector_index, connector_item in enumerate(test):
			#print connector_index, connector_item, test[connector_item]

			for test_index, test_item in enumerate(test[connector_item]):
				#for pin_index, pin_item in enumerate(test[connector_item][test_index]):
				#print "Test %s.%s - %s.%s" % (connector_item,test_item[0],connector_item,test_item[1])
		
				#TEST A pin su anodo alto
				#  Il pin sul catodo deve valere 1

				pin_out = ablib.Pin(connector_item+test_item[0],'HIGH')
				pin_in = ablib.Pin(connector_item+test_item[1],'INPUT')

				if pin_in.get_value()<>1:
					print "TEST A: Pin %s.%s o %s.%s in corto verso massa" % (connector_item,test_item[0],connector_item,test_item[1])
					error_counter = error_counter + 1

				#TEST B pin su anodo basso
				#  Il pin sul catodo deve valere 1

				pin_out = ablib.Pin(connector_item+test_item[0],'LOW')
				pin_in = ablib.Pin(connector_item+test_item[1],'INPUT')

				if pin_in.get_value()<>1:
					print "TEST B: Pin %s.%s e %s.%s in corto" % (connector_item,test_item[0],connector_item,test_item[1])
					error_counter = error_counter + 1

				#TEST C pin su catodo basso
				#  Il pin sul anodo deve valere 0

				pin_in = ablib.Pin(connector_item+test_item[0],'INPUT')
				pin_out = ablib.Pin(connector_item+test_item[1],'LOW')
			
				if pin_in.get_value()<>0:
					print "TEST C: Pin %s.%s o %s.%s staccati" % (connector_item,test_item[0],connector_item,test_item[1])
					error_counter = error_counter + 1

				#TEST D pin su catodo alto
				#  Il pin sul anodo deve valere 1

				pin_in = ablib.Pin(connector_item+test_item[0],'INPUT')
				pin_out = ablib.Pin(connector_item+test_item[1],'HIGH')

				if pin_in.get_value()<>1:
					print "TEST D: Pin %s.%s o %s.%s in corto verso massa" % (connector_item,test_item[0],connector_item,test_item[1])
					error_counter = error_counter + 1
				# ripristina il pin di uscita in ingresso
				pin_out = ablib.Pin(connector_item+test_item[1],'INPUT')

		if error_counter==0:
			break
		else:
			LEDR = ablib.Pin('N23','HIGH')
			LEDG = ablib.Pin('N22','LOW')
			time.sleep(1)

	print color_pass + "GPIO test OK" + color_normal

else:
	print color_check + "Test N21 (PC19) is LOW: no GPIO test done" + color_normal



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





