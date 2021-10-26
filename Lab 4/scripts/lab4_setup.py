from datetime import datetime
import qwiic_oled_display
import sys
import time
from speech2text_pt2 import speech2text
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import adafruit_rgb_display.st7789 as st7789
from adafruit_rgb_display.rgb import color565

### OLED Display
# Initialize OLEDs
myOLED = qwiic_oled_display.QwiicOledDisplay()
def runDisplay():

    #  These lines of code are all you need to initialize the OLED display and print text on the screen.
    myOLED.begin()

    # print("\nSparkFun Qwiic OLED Display - Hello Example\n")

    if myOLED.is_connected() == False:
        print("The Qwiic OLED Display isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        return
    
    #  Before you can start using the OLED, call begin() to init all of the pins and configure the OLED.

    myOLED.clear(myOLED.PAGE)  #  Clear the display's buffer
    myOLED.set_font_type(1)

    myOLED.print(time.strftime("%I:%M:%S %p"))  #  Add "Hello World" to buffer

    #  To actually draw anything on the display, you must call the display() function. 
    myOLED.display()

# while True:
#     runDisplay()
#     time.sleep(1)

### Convert time
def time_diff(start, end):
    """
    Converting military time in string format to time difference in hours and minutes

    Input:
    Start time in hours: mins: sec format
    End time in hours: mins: sec format

    Output:
    Time difference in hours: mins
    """
    format = '%H:%M:%S'
    t_delta = datetime.strptime(end, format) - datetime.strptime(start, format)
    hrs_delta = t_delta.seconds // 3600
    mins_delta = (t_delta.seconds - hrs_delta * 3600) // 60

    return f'{hrs_delta} hours and {mins_delta} minutes'

### Text to Speech
def alarm_speech(hrs_slept = None):
    cur_time = time.strftime("%I:%M %p")
    sleep_hr = '5'
    cmd = '''
                say() { local IFS=+;/usr/bin/mplayer -ao alsa -really-quiet -noconsolecontrols "http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q=$*&tl=en"; }\
                ''' + f'''
                say "Hey it's time to wake up. Right now its {cur_time}. You've slept for {sleep_hr} hours."
                '''
    subprocess.check_output(cmd, shell=True)

### Display Weather
def display_weather():
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
    font2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)

    # Turn on the backlight
    backlight = digitalio.DigitalInOut(board.D22)
    backlight.switch_to_output()
    backlight.value = True

    cmd = 'curl -s  wttr.in/?T | head -n7 | tail -n6'
    wttr = subprocess.check_output(cmd, shell=True).decode("utf-8")

    y = top
    draw.text((x, y), wttr, font=font2, fill="#FFC300")
    y += font2.getsize(wttr)[1]
    disp.image(image, rotation)


### Display Time
# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
def display_time():    
    cs_pin = digitalio.DigitalInOut(board.CE0)
    dc_pin = digitalio.DigitalInOut(board.D25)
    reset_pin = None

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
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)

    # Turn on the backlight
    backlight = digitalio.DigitalInOut(board.D22)
    backlight.switch_to_output()
    backlight.value = True

    cur_time = time.strftime("%I:%M:%S %p")
    cur_date = datetime.strftime(datetime.now(), "%B %d, %Y")

    # for i in range(10):
        # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    y = top
    draw.text((x, y), cur_date, font=font, fill="#FFFFFF")
    y += font.getsize(cur_date)[1]
    draw.text((x, y), cur_time, font=font, fill="#00FF00")
    y += font.getsize(cur_time)[1]
    # Display image.
    disp.image(image, rotation)
    time.sleep(1)

    # backlight.value = False
    