#!/usr/bin/python
#Adeguato per il test inproduzione

import time
import fox
import serial
import sys
import os

# Test GPIO

print "Test GPIO"

test = { 
	"J6" : [
		["3","4"],
		["5","6"],
		["7","8"],
		["9","10"],
		["13","14"],
		["15","16"],
		["17","18"],
		["19","20"],
		["21","22"],
		["24","36"],
		["25","26"],
		["27","28"],
		["29","30"],
		["31","32"],
		["37","38"],
	],
	"J7" : [
		["3",  "4"],
		["5",  "6"],
		["7",  "8"],
		["9", "10"],
		["11","12"],
		["13","14"],
		["15","16"],
		["17","18"],
 		["21","22"],
 		["31","32"],
 		["33","34"],
 		["35","36"],
 		["37","38"],
 
	],
}

error_counter=0
for connector_index, connector_item in enumerate(test):
	#print connector_index, connector_item, test[connector_item]
	for test_index, test_item in enumerate(test[connector_item]):
		#for pin_index, pin_item in enumerate(test[connector_item][test_index]):
		print "Test %s.%s - %s.%s" % (connector_item,test_item[0],connector_item,test_item[1])

		pin_out = fox.Pin(connector_item,test_item[0],'low')
		pin_in = fox.Pin(connector_item,test_item[1],'in')

		if pin_in.get_value()<>0:
			print "gpio error %s.%s = low ->  %s.%s" % (connector_item,test_item[0],connector_item,test_item[1])
			error_counter = error_counter + 1

		pin_out = fox.Pin(connector_item,test_item[0],'high')
		pin_in = fox.Pin(connector_item,test_item[1],'in')

		if pin_in.get_value()<>1:
			print "gpio error %s.%s = high ->  %s.%s" % (connector_item,test_item[0],connector_item,test_item[1])
			error_counter = error_counter + 1

		pin_out = fox.Pin(connector_item,test_item[1],'low')
		pin_in = fox.Pin(connector_item,test_item[0],'in')

		if pin_in.get_value()<>0:
			print "gpio error %s.%s = low ->  %s.%s" % (connector_item,test_item[1],connector_item,test_item[0])
			error_counter = error_counter + 1

		pin_out = fox.Pin(connector_item,test_item[1],'high')
		pin_in = fox.Pin(connector_item,test_item[0],'in')

		if pin_in.get_value()<>1:
			print "gpio error %s.%s = high ->  %s.%s" % (connector_item,test_item[1],connector_item,test_item[0])
			error_counter = error_counter + 1

if error_counter==0:
	print "GPIO test OK"
else:
	print "GPIO test KO"

os.system("rm index.html");
os.system("wget http://www.acmesystems.it");



