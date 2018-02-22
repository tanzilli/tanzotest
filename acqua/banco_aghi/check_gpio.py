import time
import acmepins
import sys
import os
import subprocess

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
	["PE16","PE17"],
	["PE18","PE19"],
	["PE23","PE15"],
	["PE25","PE24"],
	["PE20","PE26"],
]

i=0
for test in testlist:
	print i,test[0],test[1]
	i=i+1
	acmepins.setup(test[0],acmepins.OUT,0)
	acmepins.setup(test[1],acmepins.IN,0)
