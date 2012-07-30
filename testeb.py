#import ablib
import time
import serial
 
ser = serial.Serial(
	port='/dev/ttyS1', 
	baudrate=115200, 
	timeout=1,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS
)  

def menu():
	print ""
	print "Test ARIAG25-EB"
	print "----------------------"
	print "1 - Quectel ON" 
	print "2 - Quectel OFF" 
	print "3 - Send AT"
	print "x - Esci" 
	print "----------------------"
 
 
#quectel_power = ablib.Pin('W','10','low')

while True:
	menu()
	scelta=raw_input("Scegli:")
	print " "

	if scelta=="1":
		print "Accendo il Quectel"
		#quectel_power.on()

	if scelta=="2":
		print "Spengo il Quectel"
		#quectel_power.off()

	if scelta=="3":
		ser.write("AT\r")
		s = ser.read(10)
		print s
		ser.close()
		
	if scelta=="x":
		print "Addio mondo crudele !"
		quit()



