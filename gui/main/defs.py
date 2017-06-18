print('defs.py')
import math
import os
import pygame as pg

#read from and write to setting file
#read settings and assign to variables
def readSettings():
    import json
    with open(setting_file_path, 'r') as data_file:
        data = json.load(data_file)
        return data
#return a given setting
def getSetting(setting):
    import json
    global testHeight, testPlot, testNote
    with open(setting_file_path, 'r') as data_file:
        data = json.load(data_file)
        return data[setting]
def saveSetting(setting, value):
    import json
    with open(setting_file_path, 'r+') as data_file:
        data = json.load(data_file)
        data[setting] = value
        data_file.seek(0)
        json.dump(data, data_file,indent=4)
        data_file.truncate()

# if __name__ == "__main__":
#critical paths
APP_PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
MAINAPP_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)))
USB_TEST_FOLDERS_PATH = '/media/cropDevUsb'#'../tests'
RASPI_TEST_FOLDERS_PATH = '/home/pi/Documents/cropDevUsb'#'../tests'
TEST_FOLDER_PATH = '/tests'
#setting file
setting_file_path = MAINAPP_PATH + '/appData.json'

# Screen Geometry
#in pixels
pg.init()
FULLSCREEN = 0
infoObject = pg.display.Info()
width = infoObject.current_w/2
height = infoObject.current_h/2
# width = 640
# height = 480
px = width/100.0
py = height/100.0
#in inches
diagonalIn = 7
witdthIn = width * diagonalIn/(math.sqrt(width**2+height**2))#
heightIn = height * diagonalIn/(math.sqrt(width**2+height**2))#
pxIn = witdthIn/100.0
pyIn = heightIn/100.0
dpi = width/witdthIn
# Colors
transparent = (0,0,0,100)
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
gray = (50,50,50)
light_blue = (50,50,255)
light_green = (50,255,50)
light_gray = (125,125,125)
light_red = (255,50,50)


#gen geo
xMargin = 2*px
yMargin = 2*py

#context area geo
caXDim = 75*px
caYDim = 100*py
caGeo = {'x': 62.5*px,'y':50*py,'xdim':caXDim-2*xMargin,'ydim':caYDim-2*yMargin}

#btnArea geo
btnXdim = 25*px
btnYdim = 25*py
btnAreaGeo = [{'x':12.5*px,'y':12.5*py,'xdim':btnXdim-2*xMargin,'ydim':btnYdim-2*yMargin},
       {'x':12.5*px,'y':37.5*py,'xdim':btnXdim-2*xMargin,'ydim':btnYdim-2*yMargin},
       {'x':12.5*px,'y':62.5*py,'xdim':btnXdim-2*xMargin,'ydim':btnYdim-2*yMargin},
       {'x':12.5*px,'y':87.5*py,'xdim':btnXdim-2*xMargin,'ydim':btnYdim-2*yMargin}]

#data strings
TEST_HEIGHT = 'testHeight'
TEST_PLOT = 'testPlot'
PRE_TEST_NOTES = 'preTestNotes'
POST_TEST_NOTES = 'postTestNotes'
NOTE_BANK = 'noteBank'
TEST_FOLDER = 'testFolder'
SENSORS = 'sensors'
SENSOR_BANK = 'sensorBank'
COLORS = 'colors'
DATA_CONFIRM_FREQ = 'dataConfirmFreq'
MAX_START_ANGLE = 'maxStartAngle'
VERSION = 'version'
#sensor types data strings
DS_LOAD_X = 'LOAD_X'
DS_LOAD_Y = 'LOAD_Y'
DS_IMU = 'IMU'
DS_POT = 'POT'
DS_TEMP = 'TEMP'
DS_HUM = 'HUM'

#data fields for sensor objects
SENSOR_UNIT = 'unit'
SENSOR_A = 'a'
SENSOR_B = 'b'
SENSOR_LAST = 'last'

SENSOR_FIELDS = [SENSOR_UNIT, SENSOR_A, SENSOR_B, SENSOR_LAST]

dataStrings = [TEST_HEIGHT, TEST_PLOT, PRE_TEST_NOTES, POST_TEST_NOTES,
                NOTE_BANK, TEST_FOLDER, SENSORS, SENSOR_BANK,
                 COLORS, DATA_CONFIRM_FREQ, MAX_START_ANGLE, VERSION]
#Sensors
sensorDataStrings = [DS_LOAD_X, DS_LOAD_Y, DS_IMU, DS_POT, DS_TEMP, DS_HUM]

#environemental data strings
TEMPERATURE = 'temp'
LOCATION = 'loc'
HUMIDITY = 'hum'
TIME = 'time'

#testing variables
testHeight = 0
testPlot = 0
testNote = ''
testNotes = []
noteBank = []
#test saving
testHeaders = ['PLOT', 'HEIGHT', 'PRE_TEST_NOTES', 'POST_TEST_NOTES', 'ANGLES', 'LOADS', 'TIMES']
#keyboard: num or word?
NUM = 'NUM'
WORD = 'WORD'

MAX_NOTES = 5 #max notes per test

textView_highlight_col = green#white#red
textView_neg_col = white#red
textView_pos_col = white#green
font_col_inv = white#light_green
graphBcg_col = white#light_green
graphPoint_col = black
arrow_col = white#red # org light_blue
nlWrapper_col = white
msgHeader_col = white
msgBody_col = light_gray
#conversion from 0-255 RGB to 0-1 RGB
def convertColor(color):
    return (x/255.0 for x in color)
def darkenColor(color):
    return [int(0.5*x) for x in color]
def brightenColor(color):
    return [255 if (int(2*x) % 255) < x else (int(2*x) % 255) for x in color]
    

