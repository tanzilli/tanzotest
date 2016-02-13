# ablib.py
#
# Python functions collection to easily manage the I/O lines and 
# Daisy modules with the following Acme Systems boards:
#   FOXG20
#   ARIAG25
#   ARIAG25-EB
#
# (C) 2012 Sergio Tanzilli <tanzilli@acmesystems.it>
# (C) 2012 Acme Systems srl (http://www.acmesystems.it)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

try:
	import os.path
	import smbus
	import time
except:
	pass


serial_ports = {
	'D1' :  '/dev/ttyS2',
	'D2' :  '/dev/ttyS5',
	'D3' :  '/dev/ttyS1',
	'D5' :  '/dev/ttyS6',
	'D6' :  '/dev/ttyS4',
	'D8' :  '/dev/ttyS3'
}

		
# Connectors pin assignments
# 'pin name', 'kernel id'  # pin description

aria_north = {
	'2'  :  96,
	'3'  :  97,
	'4'  :  98,
	'5'  :  99,
	'6'  : 100,
	'7'  : 101,
	'8'  : 102,
	'9' :  103,
	'10' : 104,
	'11' : 105,
	'12' : 106,
	'13' : 107,
	'14' : 108,
	'15' : 109,
	'16' : 110,
	'17' : 111,
	'18' : 112,
	'19' : 113,
	'20' : 114,
	'21' : 115,
	'22' : 116,
	'23' : 117,
}

aria_east = {
	'2'  : 118,
	'3'  : 119,
	'4'  : 120,
	'5'  : 121,
	'6'  : 122,
	'7'  : 123,
	'8'  : 124,
	'9' :  125,
	'10' : 126,
	'11' : 127,
}

aria_south = {
	'2'  :  53,
	'3'  :  52,
	'4'  :  51,
	'5'  :  50,
	'6'  :  49,
	'7'  :  48,
	'8'  :  47,
	'9' :   46,
	'10' :  45,
	'11' :  44,
	'12' :  43,
	'13' :  42,
	'14' :  41,
	'15' :  40,
	'16' :  39,
	'17' :  38,
	'18' :  37,
	'19' :  36,
	'20' :  35,
	'21' :  34,
	'22' :  33,
	'23' :  32,
}

aria_west = {
	'9' :   54,
	'10' :  55,
	'11' :  56,
	'12' :  57,
	'13' :  58,
	'14' :  59,
	'15' :  60,
	'16' :  61,
	'17' :  62,
	'18' :  63,
	'20' :  75,
	'21' :  76,
	'22' :  77,
	'23' :  78,
}

J7_kernel_ids = {
	'3'  :  82,
	'4'  :  83,
	'5'  :  80,
	'6'  :  81,
	'7'  :  66,
	'8'  :  67,
	'9'  :  64,
	'10' :  65,
	'11' : 110,
	'12' : 111,
	'13' : 108,
	'14' : 109,
	'15' : 105,
	'16' : 106,
	'17' : 103,
	'18' : 104,
	'19' : 101,
	'20' : 102,
	'21' :  73,
	'22' :  72,
	'31' :  87,
	'32' :  86,
	'33' :  89,
	'34' :  88,
	'35' :  60,
	'36' :  59,
	'37' :  58,
	'38' :  57,
}

J6_kernel_ids = {
	'3'  :  92,
	'4'  :  71,
	'5'  :  70,
	'6'  :  93,
	'7'  :  90,
	'8'  :  69,
	'9'  :  68,
	'10' :  91,
	'13' :  75,
	'14' :  74,
	'15' :  77,
	'16' :  76,
	'17' :  85,
	'18' :  84,
	'19' :  95,
	'20' :  94,
	'21' :  63,
	'22' :  62,
	'24' :  38,
	'25' :  39,
	'26' :  41,
	'27' :  99,
	'28' :  98,
	'29' :  97,
	'30' :  96,
	'31' :  56,
	'32' :  55,
	'36' :  42,
	'37' :  54,
	'38' :  43,
}


D1_kernel_ids = {
	'1' :   0, #3V3
	'2' :  70, #PB6
	'3' :  71, #PB7
	'4' :  92, #PB28
	'5' :  93, #PB29
	'6' :   0, #N.C.
	'7' :  55, #PA23
	'8' :  56, #PA24
	'9' :   0, #5V0
	'10':   0, #GND
}

D2_kernel_ids = {
	'1' :   0, #3V3
	'2' :  63, #PA31
	'3' :  62, #PA30
	'4' :  61, #PA29
	'5' :  60, #PA28
	'6' :  59, #PA27
	'7' :  58, #PA26
	'8' :  57, #PA25
	'9' :  94, #PB30
	'10':   0, #GND
}

D3_kernel_ids = {
	'1' :   0, #3V3
	'2' :  68, #PB4
	'3' :  69, #PB5
	'4' :  90, #PB26
	'5' :  91, #PB27
	'6' :  86, #PB22
	'7' :  88, #PB24
	'8' :  89, #PB25
	'9' :  87, #PB23
	'10':   0, #GND
}

D4_kernel_ids = {
	'1' :   0, #3V3
	'2' :   0, #AVDD
	'3' :   0, #VREF
	'4' :   0, #AGND
	'5' :  96, #PC0
	'6' :  97, #PC1
	'7' :  98, #PC2
	'8' :  99, #PC3
	'9' :   0, #5V0
	'10':   0, #GND
}


D5_kernel_ids = {
	'1' :   0, #3V3
	'2' :  76, #PB12
	'3' :  77, #PB13
	'4' :  80, #PB16
	'5' :  81, #PB17
	'6' :  82, #PB18
	'7' :  83, #PB19
	'8' :  84, #PB20
	'9' :  85, #PB21
	'10':  0,  #GND
}

D6_kernel_ids = {
	'1' :   0, #3V3
	'2' :  74, #PB10
	'3' :  75, #PB11
	'4' : 104, #PC8
	'5' : 106, #PC10
	'6' :  95, #PB31
	'7' :  55, #PA23
	'8' :  56, #PA24
	'9' :   0, #5V0
	'10':   0, #GND
}

D7_kernel_ids = {
	'1' :  0,  #3V3
	'2' :  65, #PB1
	'3' :  64, #PB0
	'4' :  66, #PB2
	'5' :  67, #PB3
	'6' : 101, #PC5
	'7' : 100, #PC4
	'8' :  99, #PC3
	'9' :   0, #5V0
	'10':   0, #GND
}

D8_kernel_ids = {
	'1' :   0, #3V3
	'2' :  72, #PB8
	'3' :  73, #PB9
	'4' :   0, #N.C.
	'5' :   0, #N.C.
	'6' :   0, #N.C.
	'7' :  55, #PA23
	'8' :  56, #PA24
	'9' :   0, #5V0
	'10':   0, #GND
}

#ARIAG25-EB Daisy connector D10
D10_kernel_ids = {
	'1' :   0, #3V3
	'2' : 118, #PC22
	'3' : 119, #PC23
	'4' : 120, #PC24
	'5' : 121, #PC25
	'6' : 122, #PC26
	'7' :  62, #PA30
	'8' :  63, #PA31
	'9' :   0, #5V0
	'10':   0, #GND
}

#ARIAG25-EB Daisy connector D11
D11_kernel_ids = {
	'1' :   0, #3V3
	'2' : 112, #PC16
	'3' : 113, #PC17
	'4' : 114, #PC18
	'5' : 115, #PC19
	'6' : 116, #PC20
	'7' : 117, #PC21
	'8' :  98, #PC2
	'9' :  99, #PC3
	'10':   0, #GND
}

#ARIAG25-EB Daisy connector D12
D12_kernel_ids = {
	'1' :   0, #3V3
	'2' : 104, #PC8
	'3' : 105, #PC9
	'4' : 106, #PC10
	'5' : 107, #PC11
	'6' : 108, #PC12
	'7' : 109, #PC13
	'8' : 110, #PC14
	'9' : 111, #PC15
	'10':   0, #GND
}

#ARIAG25-EB Daisy connector D13
D13_kernel_ids = {
	'1' :   0, #3V3
	'2' :  37, #PA5
	'3' :  38, #PA6
	'4' : 123, #PC27
	'5' : 124, #PC28
	'6' : 125, #PC29
	'7' :  96, #PC0
	'8' :  97, #PC1
	'9' :   0, #5V0
	'10':   0, #GND
}

#ARIAG25-EB Daisy connector D14
D14_kernel_ids = {
	'1' :   0, #3V3
	'2' :   0, #3V3
	'3' :   0, #VREF
	'4' :   0, #GND
	'5' :  75, #PB11
	'6' :  76, #PB12
	'7' :  77, #PB13
	'8' :  78, #PB14
	'9' :   0, #5V0
	'10':   0, #GND
}

#ARIAG25-EB Daisy connector D15
D15_kernel_ids = {
	'1' :   0, #3V3
	'2' :  44, #PA12
	'3' :  43, #PA11
	'4' :  45, #PA13
	'5' :  46, #PA14
	'6' :  39, #PA7
	'7' :  33, #PA1
	'8' :   0, #N.C.
	'9' :   0, #5V0
	'10':   0, #GND
}

#ARIAG25-EB Daisy connector D16
D16_kernel_ids = {
	'1' :   0, #3V3
	'2' :  56, #PA24
	'3' :  57, #PA25
	'4' :  58, #PA26
	'5' :  59, #PA27
	'6' :  60, #PA28
	'7' :  61, #PA29
	'8' :  63, #PA31.
	'9' :  62, #PA30
	'10':   0, #GND
}

# Kernel IDs descriptors for each connector
connectors = {
	'N'   :  aria_north,
	'E'   :  aria_east,
	'S'   :  aria_south,
	'W'   :  aria_west,
	'J6'  :  J6_kernel_ids,
	'J7'  :  J7_kernel_ids,
	'D1'  :  D1_kernel_ids,
	'D2'  :  D2_kernel_ids,
	'D3'  :  D3_kernel_ids,
	'D4'  :  D4_kernel_ids,
	'D5'  :  D5_kernel_ids,
	'D6'  :  D6_kernel_ids,
	'D7'  :  D7_kernel_ids,
	'D8'  :  D8_kernel_ids,
	'D10' :  D10_kernel_ids,
	'D11' :  D11_kernel_ids,
	'D12' :  D12_kernel_ids,
	'D13' :  D13_kernel_ids,
	'D14' :  D14_kernel_ids,
	'D15' :  D15_kernel_ids,
	'D16' :  D16_kernel_ids,
}

def get_kernel_id(connector_name,pin_number):
	return connectors[connector_name][pin_number]

def export(kernel_id):
	iopath='/sys/class/gpio/gpio' + str(kernel_id)
	if not os.path.exists(iopath): 
		f = open('/sys/class/gpio/export','w')
		f.write(str(kernel_id))
		f.close()

def direction(kernel_id,direct):
	iopath='/sys/class/gpio/gpio' + str(kernel_id)
	if os.path.exists(iopath): 
		f = open(iopath + '/direction','w')
		f.write(direct)
		f.close()

def set_value(kernel_id,value):
	iopath='/sys/class/gpio/gpio' + str(kernel_id)
	if os.path.exists(iopath): 
		f = open(iopath + '/value','w')
		f.write(str(value))
		f.close()

def get_value(kernel_id):
	if kernel_id<>-1:
		iopath='/sys/class/gpio/gpio' + str(kernel_id)
		if os.path.exists(iopath): 
			f = open(iopath + '/value','r')
			a=f.read()
			f.close()
			return int(a)

class Pin():
	"""
	FOX pins related class
	"""
	kernel_id=-1

	def __init__(self,connector_id,pin_name,direct):
		self.kernel_id=get_kernel_id(connector_id,pin_name)
		export(self.kernel_id)
		direction(self.kernel_id,direct)

	def on(self):
		set_value(self.kernel_id,1)
		
	def off(self):
		set_value(self.kernel_id,0)

	def set_value(self,value):
		return set_value(self.kernel_id,value)

	def get_value(self):
		return get_value(self.kernel_id)

class Daisy4():

	"""
	DAISY-4 (Relay module) related class
	http://www.acmesystems.it/?id=DAISY-4
	"""
	kernel_id=-1

	dips = {
		'DIP1' :  '2',
		'DIP2' :  '3',
		'DIP3' :  '4',
		'DIP4' :  '5',
		'DIP5' :  '6',
		'DIP6' :  '7',
		'DIP7' :  '8',
		'DIP8' :  '9',
	}

	def __init__(self,connector_id,dip_id):
		pin=self.dips[dip_id]
		self.kernel_id = get_kernel_id(connector_id,pin)

		if (self.kernel_id!=0):
			export(self.kernel_id)
			direction(self.kernel_id,'low')


	def on(self):
		if (self.kernel_id!=0):
			set_value(self.kernel_id,1)
		else:
			pass

		
	def off(self):
		if (self.kernel_id!=0):
			set_value(self.kernel_id,0)
		else:
			pass
	
	
	
class Daisy5():

	"""
	DAISY-5 (8 pushbuttons) related class
	http://www.acmesystems.it/?id=DAISY-5
	kernel_id=-1
	"""

	buttons = {
		'P1' :  '2',
		'P2' :  '3',
		'P3' :  '4',
		'P4' :  '5',
		'P5' :  '6',
		'P6' :  '7',
		'P7' :  '8',
		'P8' :  '9',
	}

	def __init__(self,connector_id,button_id):
		pin=self.buttons[button_id]
		self.kernel_id = get_kernel_id(connector_id,pin)

		if (self.kernel_id!=0):
			export(self.kernel_id)
			direction(self.kernel_id,'in')

	def pressed(self):
		if self.kernel_id<>-1:
			iopath='/sys/class/gpio/gpio' + str(self.kernel_id)
			if os.path.exists(iopath): 
				f = open(iopath + '/value','r')
				a=f.read()
				f.close()
				if int(a)==0:
					return False
				else:
					return True
		return False

	def on(self):
		if self.handler_on!=0: 
			self.handler_on()

	def off(self):
		if self.handler_off!=0: 
			self.handler_off()

class Daisy11():

	"""
	DAISY-11 (8 led) related class
	http://www.acmesystems.it/?id=DAISY-11
	"""

	kernel_id=-1

	leds = {
		'L1' :  '2',
		'L2' :  '3',
		'L3' :  '4',
		'L4' :  '5',
		'L5' :  '6',
		'L6' :  '7',
		'L7' :  '8',
		'L8' :  '9',
	}

	def __init__(self,connector_id,led_id):
		pin=self.leds[led_id]
		self.kernel_id = get_kernel_id(connector_id,pin)

		if (self.kernel_id!=0):
			export(self.kernel_id)
			direction(self.kernel_id,'low')


	def on(self):
		if (self.kernel_id!=0):
			set_value(self.kernel_id,1)
		else:
			pass

		
	def off(self):
		if (self.kernel_id!=0):
			set_value(self.kernel_id,0)
		else:
			pass

	def get(self):
		if get_value(self.kernel_id):
			return True
		else:
			return False

class Daisy15():

	"""
	DAISY-15 (4DSystems lcd display) related class
	http://www.acmesystems.it/?id=DAISY-15
	"""

	serial = None

	def __init__(self,connector_id):
		self.serial = serial.Serial(
			port=serial_ports[connector_id], 
			baudrate=9600, 
			timeout=1,
			parity=serial.PARITY_NONE,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS
		)

		self.serial.write("U")		# Autobaud char
		rtc = self.serial.read(1)	# Wait for a reply

		self.serial.write("E")		# Clear screen
		rtc = self.serial.read(1)	# Wait for a reply

	def send(self,col,row,str):
		self.serial.write("s%c%c%c%c%c%s%c" % (int(row),int(col),2,0xFF,0xFF,str,0x00))		
		rtc = self.serial.read(1)

class Daisy19():

	"""
	DAISY-19 (4 mosfet output) related class
	http://www.acmesystems.it/?id=DAISY-19
	"""

	kernel_id=-1

	outputs_first = {
		'O1' :  '2',
		'O2' :  '3',
		'O3' :  '4',
		'O4' :  '5',
	}

	outputs_second = {
		'O1' :  '6',
		'O2' :  '7',
		'O3' :  '8',
		'O4' :  '9',
	}

	def __init__(self,connector_id,position,output_id):
		if (position=="first"): 
			pin=self.outputs_first[output_id]
		else:
			pin=self.outputs_second[output_id]
			
		self.kernel_id = get_kernel_id(connector_id,pin)

		if (self.kernel_id!=0):
			export(self.kernel_id)
			direction(self.kernel_id,'low')


	def on(self):
		if (self.kernel_id!=0):
			set_value(self.kernel_id,1)
		else:
			pass

	def off(self):
		if (self.kernel_id!=0):
			set_value(self.kernel_id,0)
		else:
			pass

	def get(self):
		if get_value(self.kernel_id):
			return True
		else:
			return False

class Daisy22():

	"""
	DAISY-22 (8 bit I2C expander)
	http://www.acmesystems.it/?id=DAISY-22
	"""

	i2c_bus=-1
	i2c_address=-1
	line=-1

	def __init__(self,bus_id=0,address=0x20,line=0):
		self.i2c_bus = smbus.SMBus(bus_id)
		self.i2c_address=address
		self.line=line
		return

	def writebyte(self,value):
   		self.i2c_bus.write_byte(self.i2c_address,value)		
		return

	def readbyte(self):
		return 	self.i2c_bus.read_byte(self.i2c_address)

	def on(self):
		currentvalue=self.i2c_bus.read_byte(self.i2c_address)
   		self.i2c_bus.write_byte(self.i2c_address,currentvalue|1<<self.line)		
		return

	def off(self):
		currentvalue=self.i2c_bus.read_byte(self.i2c_address)
   		self.i2c_bus.write_byte(self.i2c_address,currentvalue&(255-(1<<self.line)))		
		return

	def get(self):
		currentvalue=self.i2c_bus.read_byte(self.i2c_address)
   		self.i2c_bus.write_byte(self.i2c_address,currentvalue|(1<<self.line))		
		linevalue=self.i2c_bus.read_byte(self.i2c_address) & (1<<self.line)
		return linevalue >> self.line

	def pressed(self):
		if self.get()==0:
			return True
		else:
			return False

class Daisy24():

	"""
	DAISY-24 (16x2 LCD module)
	http://www.acmesystems.it/?id=DAISY-24
	"""

	i2c_bus=-1
	lcd_address = 0x3E
	exp_address = -1
	backled = -1
	K0 = -1 
	K1 = -1 
	K2 = -1 
	K3 = -1 

	def __init__(self,bus_id=0,exp_address=0x27):
		self.exp_address = exp_address
		self.i2c_bus = smbus.SMBus(bus_id)
		self.sendcommand(0x38)
		self.sendcommand(0x39)
		self.sendcommand(0x14) #Internal OSC freq
		self.sendcommand(0x72) #Set contrast 
		self.sendcommand(0x54) #Power/ICON control/Contrast set
		self.sendcommand(0x6F) #Follower control
		self.sendcommand(0x0C) #Display ON
		self.clear()
		self.K0=Daisy22(bus_id,exp_address,0)
		self.K1=Daisy22(bus_id,exp_address,1)
		self.K2=Daisy22(bus_id,exp_address,2)
		self.K3=Daisy22(bus_id,exp_address,3)
		self.backled=Daisy22(bus_id,exp_address,4)
		return

	def sendcommand(self,value):
		self.i2c_bus.write_byte_data(self.lcd_address,0x00,value)
		return

	def senddata(self,value):
		self.i2c_bus.write_byte_data(self.lcd_address,0x40,value)
		return

	def clear(self):
		"""
		CLear the display content
		"""
		self.sendcommand(0x01)
		time.sleep(0.001)
		return

	def home(self):
		"""
		Place the curson at home position
		"""
		self.sendcommand(0x03)
		time.sleep(0.001)
		return

	def setcontrast(self,value):
		"""
		Set the display contrast
		value = 0 to 15
		"""
		self.sendcommand(0x70 + value)
		return

	def setdoublefont(self):
		self.sendcommand(0x30 + 0x0C + 0x01)
		return

	def setsinglefont(self):
		self.sendcommand(0x30 + 0x08 + 0x01)
		return

	def setcurpos(self,x,y):
		if y<0 or y>1:
			return
		if x<0 or x>15:
			return

		if y==0:
			self.sendcommand(0x80+0x00+x)
		else:
			self.sendcommand(0x80+0x40+x)
		return

	def putchar(self,value):
		self.senddata(value)
		return

	def putstring(self,string):
		if len(string)==0:
			return
		if len(string)>16:
			string=string[0:16]

		for char in string:
			self.putchar(ord(char))
		return

	def backlighton(self):
		self.backled.on()		
		return

	def backlightoff(self):
		self.backled.off()
		return

	def pressed(self,keyid):
		if keyid==0:
			return self.K0.pressed()
		if keyid==1:
			return self.K1.pressed()
		if keyid==2:
			return self.K2.pressed()
		if keyid==3:
			return self.K3.pressed()

		return False

#--------------------------------------------------------------

w1path = "/sys/bus/w1/devices/w1 bus master"

def w1buslist():

		if not os.path.exists(w1path): 
			print "1-wire bus not found"
			print "Check if the 1-wire bus is installed"
			return

		deviceList = os.listdir(w1path)

#		for deviceId in deviceList:
#			print deviceId

		return [deviceId[3:] for deviceId in deviceList if deviceId[0:2]=="28"]

class DS18B20():

	sensor_path=""

	def __init__(self,w1Id):
		if not os.path.exists(w1path): 
			print "1-wire bus not found"
			return

		self.sensor_path = os.path.join(w1path,"28-" + w1Id)

		if not os.path.exists(self.sensor_path): 
			print "Sensor %s not found" % (w1Id)
			return

#		print self.sensor_path

	def getTemp(self):

		f = open(self.sensor_path + '/w1_slave','r')
		tString=f.read()
		f.close()

		if tString.find("NO")>=0:
			print "Wrong CRC"
			return
			
		p=tString.find("t=")
		return float(tString[p+2:-1])/1000

class DS28EA00():

	sensor_path=""

	def __init__(self,w1Id):
		if not os.path.exists(w1path): 
			print "1-wire bus not found"
			return

		self.sensor_path = os.path.join(w1path,"42-" + w1Id)

		if not os.path.exists(self.sensor_path): 
			print "Sensor %s not found" % (w1Id)
			return

#		print self.sensor_path

	def getTemp(self):

		f = open(self.sensor_path + '/therm','r')
		tString=f.read()
		f.close()

		if tString.find("NO")>=0:
			print "Wrong CRC"
			return
			
		p=tString.find("t=")
		return float(tString[p+2:-1])

