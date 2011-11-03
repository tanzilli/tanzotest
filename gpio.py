#!/usr/bin/python

import time
import fox
import serial
import sys
import os

# Test GPIO

print "Test GPIO"

test = { 
	"J7" : [
		["3","4"],
		["5","6"]
	],
#	"J6" : [
#		[6,7],
#		[8,9]
#	],
}

for connector_index, connector_item in enumerate(test):
	#print connector_index, connector_item, test[connector_item]
	for test_index, test_item in enumerate(test[connector_item]):
		#for pin_index, pin_item in enumerate(test[connector_item][test_index]):
		#print connector_item
		#print test_item[0]
		#print test_item[1]

		pin_out = fox.Pin(connector_item,test_item[0],'low')
		pin_in = fox.Pin(connector_item,test_item[1],'in')

		if pin_in.get_value()<>0:
			print "Errore %s.%s = low ->  %s.%s" % (connector_item,test_item[0],connector_item,test_item[1])

		pin_out = fox.Pin(connector_item,test_item[0],'high')
		pin_in = fox.Pin(connector_item,test_item[1],'in')

		if pin_in.get_value()<>1:
			print "Errore %s.%s = high ->  %s.%s" % (connector_item,test_item[0],connector_item,test_item[1])

		pin_out = fox.Pin(connector_item,test_item[1],'low')
		pin_in = fox.Pin(connector_item,test_item[0],'in')

		if pin_in.get_value()<>0:
			print "Errore %s.%s = low ->  %s.%s" % (connector_item,test_item[1],connector_item,test_item[0])

		pin_out = fox.Pin(connector_item,test_item[1],'high')
		pin_in = fox.Pin(connector_item,test_item[0],'in')

		if pin_in.get_value()<>1:
			print "Errore %s.%s = high ->  %s.%s" % (connector_item,test_item[1],connector_item,test_item[0])


