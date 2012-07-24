#!/usr/bin/python
# Banco di Test per Aia G25
# Software lato Aria G25
# Author: Sergio Tanzilli - tanzilli@acmesystems.it

import time
import acmeboards
import serial
import sys
import os

#greenled PC20
#redled PC21

# Test GPIO

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
	],
}

for connector_index, connector_item in enumerate(test):
	#print connector_index, connector_item, test[connector_item]

	for test_index, test_item in enumerate(test[connector_item]):
		#for pin_index, pin_item in enumerate(test[connector_item][test_index]):
		#print "Test %s.%s - %s.%s" % (connector_item,test_item[0],connector_item,test_item[1])

		while True:
			error_counter=0

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

			pin_out = acmeboards.Pin(connector_item,test_item[1],'low')
			pin_in = acmeboards.Pin(connector_item,test_item[0],'in')

			if pin_in.get_value()<>0:
				print "TEST C: Pin %s.%s o %s.%s staccati" % (connector_item,test_item[0],connector_item,test_item[1])
				error_counter = error_counter + 1

			#TEST D pin su catodo alto
			#  Il pin sul anodo deve valere 1

			pin_out = acmeboards.Pin(connector_item,test_item[1],'high')
			pin_in = acmeboards.Pin(connector_item,test_item[0],'in')

			if pin_in.get_value()<>1:
				print "TEST D: Pin %s.%s o %s.%s in corto verso massa" % (connector_item,test_item[0],connector_item,test_item[1])
				error_counter = error_counter + 1

			if error_counter==0:
				break
			else:
				time.sleep(1)

print "GPIO test OK"
#os.system("rm index.html");
#os.system("wget http://10.55.99.2");


