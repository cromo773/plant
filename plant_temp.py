import RPi.GPIO as GPIO
import dht11
import time
from time import sleep, strftime, time
from datetime import datetime
from pathlib import Path
import Adafruit_MCP3008

dir_path = Path(__file__).parent.resolve()
data_file = dir_path/'data.csv'
logfile = dir_path/'loggerdata.log'

time.time()

def create_csv(data_file):
    with open(data_file,'w') as f:
        writer = csv.writer(f)
        header = ("Date/time","Temperature","Humidity","Soil humidity")
        writer.writerow(header)

def add_csv_data(data_file, data):
    with open (data_file, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(data)

def measure_th():
    if result.is_valid():
        add_csv_data(data_file,"Temperature:", result.temperature)
    else:
        logger.error({e.__class__.__name__}, {e})

def measure_soil():
    if result.is_valid():
        soil_value = format(value / 1023 * 100)
        add_csv_data(data_file,soil_value)
    else:
        logger.error({e.__class__.__name__}, {e})

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# Setup the switch pin
SWITCH = 20
GPIO.setup(SWITCH, GPIO.OUT)

# read temp and humidity using pin 14
instance = dht11.DHT11(pin = 7)
result = instance.read()

#print Temp and Humidity
if result.is_valid():
    print("Temperature: %-3.1f C" % result.temperature)
    print("Humidity: %-3.1f %%" % result.humidity)
else:
    print("Error: %d" % result.error_code)

# Software SPI configuration:
CLK  = 18
MISO = 23
MOSI = 24
CS   = 25
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

print("Reading MCP3008 value on channel 0, press Ctrl-C to quit...")

while True:
    # Main program loop.
    try:
        GPIO.output(SWITCH, GPIO.HIGH)
        sleep(10)
        value = float(mcp.read_adc(0))
        print("The soil moisture reading is currently at {:.2f}%").format(value / 1023 * 100)
        GPIO.output(SWITCH, GPIO.LOW)
        sleep(10)
    except KeyboardInterrupt:
        GPIO.output(SWITCH, GPIO.LOW)
        GPIO.cleanup()

#soil_humidity = {:.2f}% format(value / 1023 * 100)

for x in range(0,100):
    try:
        measure_th()
        measure_soil()
    except:
        logger.error({e.__class__.__name__}, {e})


