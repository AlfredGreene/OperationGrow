import growCommon, growConfig, growLogger, growMoisture
import serial, time
import RPi.GPIO as GPIO
import growConfig.NUM_PLANTS as NUM_PLANTS

configTable = None
mcu = None

waterGpio = [{'valve':8, 'sense':22, 'receive':7},
             {'valve':10, 'sense':22, 'receive':11},
             {'valve':12, 'sense':22, 'receive':13},
             {'valve':16, 'sense':22, 'receive':15}]
assert(len(waterGpio) >= NUM_PLANTS)

reservoirGpio = {'sense':22, 'receive':[19,21,23]}

timeLastMeasure = [0] * NUM_PLANTS

def init():
    loadConfiguration()
    connectMCU()
    initGPIO()
    mainLoop()


def loadConfiguration():
    c = growConfig.Configuration()
    configTable = c.read()


def connectMCU():
    mcu = serial.Serial(growCommon.MCU_DEVICE_NAME)
    # Sleep for 2 seconds before any communication with the Arduino
    time.sleep(2)


def initGPIO():
    # use P1 header pin numbering convention
    GPIO.setmode(GPIO.BOARD)

    for plant in waterGpio:
	GPIO.setup(plant['valve'], GPIO.OUT)
	GPIO.setup(plant['sense'], GPIO.OUT)
	GPIO.setup(plant['receive'], GPIO.IN)

    GPIO.setup(reservoirGpio['sense'], GPIO.OUT)
    for pin in reservoirGpio['receive']:
	GPIO.setup(pin, GPIO.IN)
	

def mainLoop():
    for plant in NUM_PLANTS:
	current = time.time()
		
	if (current - timeLastMeasure[plant]) > MOISTURE_MEASUREMENT_INTERVAL:
	    moisture = measureMoisture(plant)
	    
            if moisture < configTable[plant]['dry']:
                growLogger.info('Watering %s.' % configTable[plant]['name'])
                waterPlant(plant)

	time.sleep(1)


def setDryLevel(plant, dry):
    c = growConfig.Configuration()
    c.setDry(plant, dry)


def measureMoisture(plant):
    # Trigger a moisture measurement for plant
    mcu.write(plant)
    moisture = int(mcu.readline())
    
    timeLastMeasure = time.time()
    growLogger.info('Moisture of %s is %d.' % (configTable[plant]['name'], moisture))
    growMoisture.push(timeLastMeasure, moisture)

    return moisture
	

def waterPlant(plant):
    times = 0
    while True:
	setValve(plant, GPIO.HIGH)
	sleep(WATER_DURATION)
	setValve(plant, GPIO.LOW)
	sleep(WATER_INTERVAL)
	times += 1

	if checkWaterInPot(plant) or times >= WATER_MAX_TIMES:
	    break

    growLogger.info("Watered %s after %d times." % (configTable[plant]['name'], times))

		
def setValve(plant, state):
    GPIO.output(waterGpio[plant]['valve'], state)


def checkWaterInPot(plant):
    GPIO.output(waterGpio[plant]['sense'], GPIO.HIGH)
    sleep(0.1)
    isWater = GPIO.intput(waterGpio[plant]['receive'])
    GPIO.output(waterGpio[plant]['sense'], GPIO.LOW)
    return isWater
