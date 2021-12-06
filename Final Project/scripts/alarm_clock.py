from __future__ import print_function
import sys
import time

# Gazi's file
from lab4_setup import *

import board
import busio
from adafruit_bus_device.i2c_device import I2CDevice
from adafruit_apds9960.apds9960 import APDS9960
from adafruit_apds9960 import colorutility
import qwiic_joystick

from struct import pack, unpack

DEVICE_ADDRESS = 0x6f  # device address of our button
STATUS = 0x03 # register for button status
AVAILIBLE = 0x1
BEEN_CLICKED = 0x2
IS_PRESSED = 0x4

# The following is for I2C communications for the button
i2c2 = busio.I2C(board.SCL, board.SDA)
button = I2CDevice(i2c2, DEVICE_ADDRESS)

i2c = board.I2C()
apds = APDS9960(i2c)
apds.enable_color = True
myJoystick= qwiic_joystick.QwiicJoystick()

def write_register(dev, register, value, n_bytes=1):
    # Write a wregister number and value
    buf = bytearray(1 + n_bytes)
    buf[0] = register
    buf[1:] = value.to_bytes(n_bytes, 'little')
    with dev:
        dev.write(buf)

def read_register(dev, register, n_bytes=1):
    # write a register number then read back the value
    reg = register.to_bytes(1, 'little')
    buf = bytearray(n_bytes)
    with dev:
        dev.write_then_readinto(reg, buf)
    return int.from_bytes(buf, 'little')

# clear out LED lighting settings. For more info https://cdn.sparkfun.com/assets/learn_tutorials/1/1/0/8/Qwiic_Button_I2C_Register_Map.pdf
write_register(button, 0x1A, 1)
write_register(button, 0x1B, 0, 2)
write_register(button, 0x19, 0)

# Initialize the joystick
myJoystick.begin()

# Light sensor threshold
THRESHOLD= 500

# Used to make sure all devices are connected, 1 if connected, 0 if not
def connections():
    if not(myJoystick.connected):
        print("Joystick not connected")
        return 0
    else:
        return 1

# Call when alarm is set (triggered by button), returns the time the alarm was set
def set_alarm():
    t= time.strftime("%m/%d/%Y %H:%M:%S")
    start_time= t[11:19]
    return start_time

# Gets joy stick values
def joy_stick():
    # X: at rest = 496, positive direction = 1023, negative direction = 0
    # Y: at rest = 511, positive direction = 1023, negative direction = 0
    # Button: at rest = 1, clicked = 0
    # Return format: X, Y, Button
    return myJoystick.horizontal, myJoystick.vertical, myJoystick.button

# Only going to use X to change threshold, inputs should be X value of joy_stick and threshold
def change_threshold(x, threshold):
    if x > 600:
        threshold = threshold + 25
    elif x < 400:
        threshold = threshold - 25
    # Max threshold value 
    if threshold >= 1200:
        threshold = 1200
    return threshold

def get_sensor_val():
    r, g, b, c = apds.color_data
    light_lux= colorutility.calculate_lux(r, g, b)
    return light_lux

def light_sensor(THRESHOLD, start_time):

    while True:
        # create some variables to store the color data in
    
        # wait for color data to be ready
        while not apds.color_data_ready:
            time.sleep(0.005)
    
        # get the data and print the different channels
        r, g, b, c = apds.color_data
        light_lux= colorutility.calculate_lux(r, g, b)
        if light_lux >= THRESHOLD:
            print("wake up")
            # ------------ CALL ALARM FUNCTION HERE --------------
            alarm_speech(start_time)
            break;
        else:
            print("sleep")
    
        time.sleep(0.5)

# For the screen, call while(1) and the joystick function at the top to get values 

# Variables to help
case= 0
start_time= set_alarm()

# Main Loop
while(1):
    # Get joystick values, button values
    joyX, joyY, joyButton= joy_stick()
    btn_status = read_register(button, STATUS)

    # Joystick clicked
    if (joyButton == 0):
        case += 1
        case = case % 3
        # case = case % 2

    # Handle screen
    if (case == 0):
        # Time screen
        display_time()

    elif (case == 1):
        # Weather screen
        display_weather() 

    elif (case == 2):
        # Threshold screen 
        display_threshold(THRESHOLD, get_sensor_val()) 
     
    # Handle threshold changes
    THRESHOLD = change_threshold(joyX, THRESHOLD) 

    # Handle alarm
    if (btn_status&IS_PRESSED) !=0:
        write_register(button, 0x19, 255)
        start_time= set_alarm()
        # Call light_sensor
        light_sensor(THRESHOLD, start_time)

    # otherwise turn it off
    else:
        write_register(button, 0x19, 0)
    # don't slam the i2c bus
    time.sleep(0.1)



# while True:
#     try:
#         # get the button status
#         btn_status = read_register(device, STATUS)
#         print(f"AVAILIBLE: {(btn_status&AVAILIBLE != 0)} BEEN_CLICKED: {(btn_status&BEEN_CLICKED != 0)} IS_PRESSED: {(btn_status&IS_PRESSED != 0)}")
#         # if pressed light LED
#         if (btn_status&IS_PRESSED) !=0:
#             write_register(device, 0x19, 255)
#         # otherwise turn it off
#         else:
#             write_register(device, 0x19, 0)
#         # don't slam the i2c bus
#         time.sleep(0.1)
# 
#     except KeyboardInterrupt:
#         # on control-c do...something? try commenting this out and running again? What might this do
#         write_register(device, STATUS, 0)
#         break














