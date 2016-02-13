import datetime
import os
import time

#Setta il timer Linux con il valore corrente dell'RTC
os.system("hwclock --hctosys")

#Prende il tempo corrente
a = datetime.datetime.now()

#Linea di test da rimuovere
#os.system("hwclock --set --date=\"01/01/01 00:00:00\"");

#Aspetta 
time.sleep(2)

#Riprende il tempo corrente
b = datetime.datetime.now()

#Visualizza quanti secondo sono passati
c = b - a
print "Tempo passato per Linux",c.seconds,"secondi"

#Setta di nuovo il timer Linux con il valore corrente dell'RTC
os.system("hwclock --hctosys")

#Controlla se per RTC e' passato lo stesso tempo del sistema operativo
d = datetime.datetime.now() - a
print "Tempo passato per RTC",d.seconds,"secondi"

if c.seconds!=d.seconds:
	print "Errore RTC"
else:
	print "RTC Ok"

