import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789

# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
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

#setup buttons
backlight= digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value= True
buttonA= digitalio.DigitalInOut(board.D23)
buttonB= digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()



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
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)


    #TODO: Lab 2 part D work should be filled in here. You should be able to look in cli_clock.py and stats.py 
    #print(time.strftime("%m/%d/%Y %H:%M:%S"), end="", flush= True)
    #draw.text((0,top),time.strftime("%m/%d/%Y %H:%M:%S"),font= font,fill= "#0000FF")

    t= time.strftime("%m/%d/%Y %H:%M:%S")

    #11 is where the first digit of the hour starts
    #if between midnight and 4 --> black
    #if between 4 and 8 --> navy blue
    #if between 8 and 12 --> light blue
    #if between 12 and 1 --> yellow
    #if between 1 and 5 --> orange
    #if between 5 and 8 --> orangish brown
    #if between 8 and 10 --> dark brown
    #if between 10 and midnight --> black

    hr= t[11:13]  
 
    if(hr >= "00" and hr< "04"):
        draw.rectangle((0,0,width,height),outline=0, fill= "#000000")
        draw.text((width/2,height/2),"You're now in",font=font,fill= "#FFFFFF",anchor="ms")
        draw.text((width/2,(height/2)+20),"The Wee Hours",font=font,fill= "#FFFFFF",anchor="ms")     
    elif (hr >= "04" and hr < "08"):
        draw.rectangle((0,0,width,height),outline=0, fill= "#101049") 
        draw.text((width/2,height/2),"Dawn is cracking!",font=font,fill= "#FFFFFF",anchor="ms")       
    elif (hr >= "08" and hr < "12"):
        draw.rectangle((0,0,width,height),outline=0, fill= "#25c0e4")  
        draw.text((width/2,height/2),"GOOD MORNING!",font=font,fill= "#f3bcee",anchor="ms")      
    elif (hr >= "12" and hr < "13"): 
        draw.rectangle((0,0,width,height),outline=0, fill= "#e8f93e")  
        draw.text((width/2,height/2),"It's NOON",font=font,fill= "#ca070b",anchor="ms")      	 
    elif (hr >= "13" and hr < "17"):
        draw.rectangle((0,0,width,height),outline=0, fill= "#f9a848")
        draw.text((width/2,height/2),"The afternoon",font=font,fill= "#FFFFFF",anchor="ms")      	
    elif (hr >= "17" and hr < "20"):
        draw.rectangle((0,0,width,height),outline=0, fill= "#9e6623")  
        draw.text((width/2,height/2),"Dinner time",font=font,fill= "#FFFFFF",anchor="ms")      	
    elif (hr >= "20" and hr < "22"):
        draw.rectangle((0,0,width,height),outline=0, fill= "#621f07")  
        draw.text((width/2,height/2),"It's starting to get late....",font=font,fill= "#FFFFFF",anchor="ms")      
    elif (hr >= "22" and hr < "24"):
        draw.rectangle((0,0,width,height),outline=0, fill= "#000000")  
        draw.text((width/2,height/2),"Less than 2 hours",font=font,fill= "#FFFFFF",anchor="ms")      
        draw.text((width/2,(height/2)+20),"from midnight!",font=font,fill= "#FFFFFF",anchor="ms")      



    print(buttonA.value)
    print("break")
    print(buttonB.value)

    count= 0
 
    tst= 1 
    if not(buttonA.value) or not(buttonB.value):
        tst= 0   
 
    while(tst == 0):
  
        print("enter") 
        if not(buttonA.value) and not(buttonB.value):
            count= count + 1
            count= count % 8
            print("here") 
        elif (not(buttonA.value)):
            count= count + 1
            count= count % 8
            print("here2") 
        elif (not(buttonB.value)):
            tst= 1 
            print("here3") 
     
        if (count == 0):
            draw.rectangle((0,0,width,height),outline=0, fill= "#000000")
            draw.text((width/2,height/2),"You're now in",font=font,fill= "#FFFFFF",anchor="ms")
            draw.text((width/2,(height/2)+20),"The Wee Hours",font=font,fill= "#FFFFFF",anchor="ms")     
        elif (count == 1):
            draw.rectangle((0,0,width,height),outline=0, fill= "#101049") 
            draw.text((width/2,height/2),"Dawn is cracking!",font=font,fill= "#FFFFFF",anchor="ms")       
        elif (count == 2):
            draw.rectangle((0,0,width,height),outline=0, fill= "#25c0e4")  
            draw.text((width/2,height/2),"GOOD MORNING!",font=font,fill= "#f3bcee",anchor="ms")      
        elif (count == 3): 
            draw.rectangle((0,0,width,height),outline=0, fill= "#e8f93e")  
            draw.text((width/2,height/2),"It's NOON",font=font,fill= "#ca070b",anchor="ms")      	 
        elif (count == 4):
            draw.rectangle((0,0,width,height),outline=0, fill= "#f9a848")
            draw.text((width/2,height/2),"The afternoon",font=font,fill= "#FFFFFF",anchor="ms")      	
        elif (count == 5):
            draw.rectangle((0,0,width,height),outline=0, fill= "#9e6623")  
            draw.text((width/2,height/2),"Dinner time",font=font,fill= "#FFFFFF",anchor="ms")      	
        elif (count == 6):
            draw.rectangle((0,0,width,height),outline=0, fill= "#621f07")  
            draw.text((width/2,height/2),"It's starting to get late....",font=font,fill= "#FFFFFF",anchor="ms")      
        elif (count == 7):
            draw.rectangle((0,0,width,height),outline=0, fill= "#000000")  
            draw.text((width/2,height/2),"Less than 2 hours",font=font,fill= "#FFFFFF",anchor="ms")      
            draw.text((width/2,(height/2)+20),"from midnight!",font=font,fill= "#FFFFFF",anchor="ms")      
     




 
    # Display image.
    disp.image(image, rotation)
    time.sleep(1)
