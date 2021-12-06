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


def speech():

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

            time.sleep(0.2)

            cmd = '''
                    say() { local IFS=+;/usr/bin/mplayer -ao alsa -really-quiet -noconsolecontrols "http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q=$*&tl=en"; }\
                    ''' + f'''
                    say "Is there anything else?"
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
            
            time.sleep(0.2)
            
            cmd = '''
                    say() { local IFS=+;/usr/bin/mplayer -ao alsa -really-quiet -noconsolecontrols "http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q=$*&tl=en"; }\
                    ''' + f'''
                    say "Is there anything else?"
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

            time.sleep(0.2)
            
            cmd = '''
                    say() { local IFS=+;/usr/bin/mplayer -ao alsa -really-quiet -noconsolecontrols "http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q=$*&tl=en"; }\
                    ''' + f'''
                    say "Is there anything else?"
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

        time.sleep(0.2)
            
        cmd = '''
                say() { local IFS=+;/usr/bin/mplayer -ao alsa -really-quiet -noconsolecontrols "http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q=$*&tl=en"; }\
                ''' + f'''
                say "Is there anything else?"
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
    time.sleep(0.5)