#!/usr/bin/env python
import time
import os
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
DEBUG = 1

# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
        if ((adcnum > 7) or (adcnum < 0)):
                return -1
        GPIO.output(cspin, True)

        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin, False)     # bring CS low

        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
                if (commandout & 0x80):
                        GPIO.output(mosipin, True)
                else:
                        GPIO.output(mosipin, False)
                commandout <<= 1
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)

        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
                adcout <<= 1
                if (GPIO.input(misopin)):
                        adcout |= 0x1

        GPIO.output(cspin, True)
        
        adcout >>= 1       # first bit is 'null' so drop it
        return adcout

# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
SPICLK = 18
SPIMISO = 23
SPIMOSI = 24
SPICS = 25

# set up the SPI interface pins
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

# Pressure sensor is connected to adc #0
pressure_adc = 1;

# Make sure the sensor is really detecting a car 
last_read = 0       
tolerance = 5       

#pressure_reading = readadc(pressure_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)
#print pressure_reading


while True:
        # we'll assume that the pot didn't move
        pressure_sensor_changed = False

        # read the analog pin
        pressure_sensor = readadc(pressure_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)
        # how much has it changed since the last read?
        pressure_adjust = abs(pressure_sensor - last_read)

        if DEBUG:
                print "pressure_sensor:", pressure_sensor
                print "pressure_adjust:", pressure_adjust
                print "last_read", last_read

        if ( pot_adjust > tolerance ):
               pressure_sensor_changed = True

        if DEBUG:
                print "pressure_sensor_changed", pressure_sensor_changed
'''
        if ( pressure_sensor_changed ):
                set_volume = trim_pot / 10.24           # convert 10bit adc0 (0-1024) trim pot read into 0-100 volume level
                set_volume = round(set_volume)          # round out decimal value
                set_volume = int(set_volume)            # cast volume as integer

                print 'Volume = {volume}%' .format(volume = set_volume)
                set_vol_cmd = 'sudo amixer cset numid=1 -- {volume}% > /dev/null' .format(volume = set_volume)
                os.system(set_vol_cmd)  # set volume


                if DEBUG:
                        print "set_volume", set_volume
                        print "tri_pot_changed", set_volume
'''
        # save the potentiometer reading for the next loop
        last_read = pressure_sensor
        # hang out and do nothing for a half second
        time.sleep(0.5)
