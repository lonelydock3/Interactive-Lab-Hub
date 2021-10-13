
# imports
import time
import board
import busio
import adafruit_apds9960.apds9960

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_apds9960.apds9960.APDS9960(i2c)


# enable proximity reading
sensor.enable_proximity = True

# print(sensor.proximity)

# get prox value --> higher the number = closer the object
while (1):
    print(sensor.proximity)

