
# imports
import time
import board
import busio
import adafruit_apds9960.apds9960

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_apds9960.apds9960.APDS9960(i2c)


# enable proximity reading
sensor.enable_proximity = True

# get prox value --> higher the number = closer the object
while (sensor.proximity == 0):
    print("I'm sleeping")

print("awake")
