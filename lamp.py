import time
from macpath import split

from bluepy.btle import Peripheral, BTLEException
import random
import urllib
import traceback


def convert(int_value):
   encoded = format(int_value, 'x')

   length = len(encoded)
   encoded = encoded.zfill(length+length%2)

   return encoded.decode('hex')

def create_color(red, green, blue):
    return "\x56" + convert(red) + convert(green) + convert(blue) + "\x00\xf0\xaa"

def start_new_display(c):
    c.write(create_color(0, 255, 0))
    time.sleep(0.5)
    c.write(create_color(0, 0, 0))
    time.sleep(0.3)
    c.write(create_color(0, 255, 0))
    time.sleep(0.5)
    print "reset"

# Delft
buien_radar = "http://gadgets.buienradar.nl/data/raintext/?lat=52.0&lon=4.21"

f = urllib.urlopen(buien_radar)
myfile = f.read()
print myfile

p = Peripheral("F8:1D:78:60:0A:85")
services = p.getServices()
for s in services:
    print "Service " + str(s)
    try:
        characteristics = s.getCharacteristics()
        print characteristics
        for c in characteristics:
            print c.propertiesToString()
            properties = c.propertiesToString()
            if "WRITE" in properties:
                print "writable!"
                start_new_display(c)
                for line in myfile.split("\n"):
                    line = line.strip()
                    if not line:
                        print "passed"
                        break

                    print line
                    rain = int(line.split("|")[0])/100*255
                    print "And rain is: " + str(rain)
                    send = create_color(0, 0, rain)
                    c.write(send, True)
                    time.sleep(0.2)
                start_new_display(c)

                for i in range(0,255,1):
                    if i % 3 == 0:
                        send = create_color(i, 0, 0)
                        c.write(send, True)
                        print send.encode('hex')
                        time.sleep(0.001)

    except :
        print("Blueteeth exception!")
        traceback.print_exc()
p.disconnect()

