#!/usr/bin/env python
import time
import os
import RPi.GPIO as GPIO
from datetime import datetime

GPIO.setmode(GPIO.BCM)

# Set the location for the CSV file
CSV_folder = '/home/pi/csv/'
CSV_file = 'output.csv'

wheel_delay = 50 # milliseconds to make sure to catch both tires

#enable debugging to get more console output
DEBUG = 1

# Make sure the sensor is really detecting a car
tolerance = 10
last_read = 0

# Pressure sensor is connected to adc #1
# Note: adc pins are 0-7
pressure_adc = 1;

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
SPICS = 31

# set up the SPI interface pins
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

# Open CSV file for writing (append mode)
f = open('%s%s'%(CSV_folder, CSV_file)), 'a')


while True:
        # we'll assume that a car is not driving over when starting
        pressure_sensor_changed = False

        # read the analog pin
        pressure_sensor = readadc(pressure_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)

        # how much has it changed since the last read?
        pressure_adjust = abs(pressure_sensor - last_read)

        if DEBUG:
                print "pressure_sensor:", pressure_sensor
                print "pressure_adjust:", pressure_adjust
                print "last_read", last_read

        if ( pressure_adjust > tolerance ):
            if (strike_number == 0):
                firstwheel =  datetime.now()
                strike_number = 1

            elif (strike_number == 1):
                secondwheel = datetime.now()
                strike_number = 0


               #pressure_sensor_changed = True

               # CSV Format: date,time,pressure
               #csv_line =

        if DEBUG:
                print "pressure_sensor_changed", pressure_sensor_changed

        # save the potentiometer reading for the next loop
        last_read = pressure_sensor
        # hang out and do nothing for a half second
        time.sleep(0.5)
