import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import adafruit_rgb_display.st7789 as st7789
from adafruit_rgb_display.rgb import color565
import adafruit_apds9960.apds9960
from time import strftime, sleep
from datetime import datetime
import busio
import json
from adafruit_bus_device.i2c_device import I2CDevice
from struct import pack, unpack
from speech2text_pt2 import speech2text
import random

# IR Sensor Setup
i2c = busio.I2C(board.SCL, board.SDA)
mpu = adafruit_apds9960.apds9960.APDS9960(i2c)
mpu.enable_proximity = True

# # For button setup
# DEVICE_ADDRESS = 0x6f  # device address of our button
# STATUS = 0x03 # reguster for button status
# AVAILIBLE = 0x1
# BEEN_CLICKED = 0x2
# IS_PRESSED = 0x4

# # The follow is for I2C communications
# i2c = busio.I2C(board.SCL, board.SDA)
# device = I2CDevice(i2c, DEVICE_ADDRESS)

# def write_register(dev, register, value, n_bytes=1):
#     # Write a wregister number and value
#     buf = bytearray(1 + n_bytes)
#     buf[0] = register
#     buf[1:] = value.to_bytes(n_bytes, 'little')
#     with dev:
#         dev.write(buf)

# def read_register(dev, register, n_bytes=1):
#     # write a register number then read back the value
#     reg = register.to_bytes(1, 'little')
#     buf = bytearray(n_bytes)
#     with dev:
#         dev.write_then_readinto(reg, buf)
#     return int.from_bytes(buf, 'little')

# # clear out LED lighting settings. For more info https://cdn.sparkfun.com/assets/learn_tutorials/1/1/0/8/Qwiic_Button_I2C_Register_Map.pdf
# write_register(device, 0x1A, 1)
# write_register(device, 0x1B, 0, 2)
# write_register(device, 0x19, 0)


# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# these setup the code for our buttons and the backlight and tell the pi to treat the GPIO pins as digitalIO vs analogIO
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font1 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
font2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

# locations
loc_dict = {
    'New York': 'newyork',
    'new york': 'newyork',
    'Hoboken': 'hoboken',
    'hoboken': 'hoboken',
    'Ithaca': 'ithaca',
    'ithaca': 'ithaca',
    'current': 'T'
}


greetings = [
    'Hey, whats up?',
    'How can I help?',
    'Nice to see you again, whats new?'
]

while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    try:
        # get the button status
        # btn_status = read_register(device, STATUS)
        # # print(f"AVAILIBLE: {(btn_status&AVAILIBLE != 0)} BEEN_CLICKED: {(btn_status&BEEN_CLICKED != 0)} IS_PRESSED: {(btn_status&IS_PRESSED != 0)}")
        # # if pressed light LED
        # if (btn_status&IS_PRESSED) !=0:
        #     write_register(device, 0x19, 255)
        if mpu.proximity > 150:
                # Reply
            cmd = '''
            say() { local IFS=+;/usr/bin/mplayer -ao alsa -really-quiet -noconsolecontrols "http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q=$*&tl=en"; }\
            ''' + f'''
            say "{greetings[random.randint(0,2)]}"
            '''
            subprocess.check_output(cmd, shell=True)
            cmd = '''
            arecord -D hw:3,0 -f cd -c1 -r 48000 -d 5 -t wav Reply.wav
            '''
            response = subprocess.check_output(cmd, shell=True)
            reply = speech2text()
            
            if 'weather' in reply:
                for loc in loc_dict.keys():
                    if loc in reply:
                        loc_short = loc_dict[loc]
                        loc_main = loc
                    else:
                        loc_short = ''
                cmd = f'curl -s  wttr.in/?T{loc_short} | head -n7 | tail -n6'
                wttr = subprocess.check_output(cmd, shell=True).decode("utf-8")
                cmd = f'curl -s  wttr.in/{loc_short}?format=j1'
                summary = json.loads(subprocess.check_output(cmd, shell=True).decode("utf-8"))
                # summary = json.loads(summary)
                if 'today' in reply:
                    max_temp = summary['weather'][0]['maxtempF']
                    min_temp = summary['weather'][0]['mintempF']

                    # chance of rain average
                    rain_chance = []
                    sunny_chance = []
                    for d in summary['weather'][0]['hourly']:
                        rain_chance.append(int(d['chanceofrain']))
                        sunny_chance.append(int(d['chanceofsunshine']))
                    rain_chance = sum(rain_chance)/len(rain_chance)
                    sunny_chance = sum(sunny_chance)/len(sunny_chance)

                    cmd = '''
                        say() { local IFS=+;/usr/bin/mplayer -ao alsa -really-quiet -noconsolecontrols "http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q=$*&tl=en"; }\
                        ''' + f'''
                        say "Today's highest temperature at {loc_main} is {max_temp} degree Fahrenheit and lowest is {min_temp}.\
                            Chances of rain at {loc_main} today is {rain_chance} percent."
                        '''
                    subprocess.check_output(cmd, shell=True).decode("utf-8")

                    cmd = '''
                    arecord -D hw:3,0 -f cd -c1 -r 48000 -d 5 -t wav Reply.wav
                    '''
                    response = subprocess.check_output(cmd, shell=True)
                    followup = speech2text()
                    
                    if 'thank you' in followup:
                        cmd = '''
                            say() { local IFS=+;/usr/bin/mplayer -ao alsa -really-quiet -noconsolecontrols "http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q=$*&tl=en"; }\
                            ''' + f'''
                            say "No problem!"
                            '''
                        subprocess.check_output(cmd, shell=True).decode("utf-8")

                elif 'day after tomorrow' in reply:
                    max_temp = summary['weather'][2]['maxtempF']
                    min_temp = summary['weather'][2]['mintempF']

                    # chance of rain average
                    rain_chance = []
                    sunny_chance = []
                    for d in summary['weather'][2]['hourly']:
                        rain_chance.append(int(d['chanceofrain']))
                        sunny_chance.append(int(d['chanceofsunshine']))
                    rain_chance = sum(rain_chance)/len(rain_chance)
                    sunny_chance = sum(sunny_chance)/len(sunny_chance)

                    cmd = '''
                        say() { local IFS=+;/usr/bin/mplayer -ao alsa -really-quiet -noconsolecontrols "http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q=$*&tl=en"; }\
                        ''' + f'''
                        say "Highest temperature at {loc_main} day after tomorrow is {max_temp} degree Fahrenheit and lowest is {min_temp}.\
                            Chances of rain at {loc_main} day after tomorrow is {rain_chance} percent."
                        '''
                    subprocess.check_output(cmd, shell=True).decode("utf-8")

                    cmd = '''
                    arecord -D hw:3,0 -f cd -c1 -r 48000 -d 5 -t wav Reply.wav
                    '''
                    response = subprocess.check_output(cmd, shell=True)
                    followup = speech2text()
                    
                    if 'thank you' in followup:
                        cmd = '''
                            say() { local IFS=+;/usr/bin/mplayer -ao alsa -really-quiet -noconsolecontrols "http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q=$*&tl=en"; }\
                            ''' + f'''
                            say "No problem!"
                            '''
                        subprocess.check_output(cmd, shell=True).decode("utf-8")

                elif 'tomorrow' in reply:
                    max_temp = summary['weather'][1]['maxtempF']
                    min_temp = summary['weather'][1]['mintempF']

                    # chance of rain average
                    rain_chance = []
                    sunny_chance = []
                    for d in summary['weather'][1]['hourly']:
                        rain_chance.append(int(d['chanceofrain']))
                        sunny_chance.append(int(d['chanceofsunshine']))
                    rain_chance = sum(rain_chance)/len(rain_chance)
                    sunny_chance = sum(sunny_chance)/len(sunny_chance)

                    cmd = '''
                        say() { local IFS=+;/usr/bin/mplayer -ao alsa -really-quiet -noconsolecontrols "http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q=$*&tl=en"; }\
                        ''' + f'''
                        say "Tomorrow's highest temperature at {loc_main} is {max_temp} degree Fahrenheit and lowest is {min_temp}.\
                            Chances of rain at {loc_main} tomorrow is {rain_chance} percent."
                        '''
                    subprocess.check_output(cmd, shell=True).decode("utf-8")
                    
                    cmd = '''
                    arecord -D hw:3,0 -f cd -c1 -r 48000 -d 5 -t wav Reply.wav
                    '''
                    response = subprocess.check_output(cmd, shell=True)
                    followup = speech2text()
                    
                    if 'thank you' in followup:
                        cmd = '''
                            say() { local IFS=+;/usr/bin/mplayer -ao alsa -really-quiet -noconsolecontrols "http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q=$*&tl=en"; }\
                            ''' + f'''
                            say "No problem!"
                            '''
                        subprocess.check_output(cmd, shell=True).decode("utf-8")

            elif 'calendar' in reply:
                cmd = '''
                    say() { local IFS=+;/usr/bin/mplayer -ao alsa -really-quiet -noconsolecontrols "http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q=$*&tl=en"; }\
                    ''' + f'''
                    say "You have an event on Saturday at Catskills. Highest temperature there would be 64 degree Fahrenheit and lowest will be 50 degree Fahrenheit."
                    '''
                subprocess.check_output(cmd, shell=True).decode("utf-8")

                cmd = '''
                    say() { local IFS=+;/usr/bin/mplayer -ao alsa -really-quiet -noconsolecontrols "http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q=$*&tl=en"; }\
                    ''' + f'''
                    say "You could see some rain, so, I recommend taking an umbrella and jacket with you for the trip."
                    '''
                subprocess.check_output(cmd, shell=True).decode("utf-8")


                cmd = '''
                    arecord -D hw:3,0 -f cd -c1 -r 48000 -d 5 -t wav Reply.wav
                    '''
                response = subprocess.check_output(cmd, shell=True)
                followup = speech2text()
                
                if 'thank you' in followup:
                    cmd = '''
                        say() { local IFS=+;/usr/bin/mplayer -ao alsa -really-quiet -noconsolecontrols "http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q=$*&tl=en"; }\
                        ''' + f'''
                        say "You're welcome! Goodbye!"
                        '''
                    subprocess.check_output(cmd, shell=True).decode("utf-8")

            else:
                wttr = ''
            y = top
            draw.text((x, y), wttr, font=font2, fill="#FFC300")
            y += font2.getsize(wttr)[1]
            disp.image(image, rotation)
        # otherwise turn it off
        else:
            pass
            # write_register(device, 0x19, 0)
        # don't slam the i2c bus
        time.sleep(1)

    except KeyboardInterrupt:
        # on control-c do...something? try commenting this out and running again? What might this do
        write_register(device, STATUS, 0)
        break
