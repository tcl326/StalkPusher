'''
testingView.py created by Witold on 2/5/2017 under the cropDevice project
TEST FILE FORMAT
NAME: 2017-12-27-11:15:28
HEADERS: PLOT | HEIGHT | PRE_TEST_NOTES | POST_TEST_NOTES | ANGLE | lOAD_X | LOAD_Y | MILLIS | TEMPERATURE | HUMIDITY | LOCATION
'''
import os
import pygame as pg
import numpy as np
# import pandas as pd
import time as t
import csv
from random import randint as ri
import defs as d
from hardware import hdInterface2 as hd
from views import view as v
from items import graph as g
from items import noteList as nl
from items import rectLabel as rl
from utils import text as txt
from views import keyboardView as kbv
from items import message as msg
from utils import postProcess as pp
preTest = 0
inTest = 1
postTest = 2


class TestingView(v.View):
    def __init__(self, app, prevView = None):
        self.title = 'TESTING'
        self.btnDefs = [
                (
                    {'label': 'START', 'id': 'startBtn', 'funct': self.startTest},
                    {'label': 'TESTS', 'id': 'testFilesBtn', 'funct': self.toTestFiles},
                    {'label': 'EDIT', 'id': 'editBtn', 'funct': self.edit},
                    {'label': 'BACK', 'id': 'bckBtn', 'funct': self.back}
                ),
                (
                    {},
                    {'label': 'STOP', 'id': 'stopBtn', 'funct': self.stopTest},
                    {},
                    {}
                ),
                (
                    {'label':'BREAK\nHEIGHT', 'id':'selectBtn', 'funct':self.setBreakHeight},
                    {'label':'SELECT', 'id':'selectBtn', 'funct':self.selectBtn},
                    {'label': 'SAVE', 'id': 'saveBtn', 'funct': self.save},
                    {'label': 'REJECT', 'id': 'bckBtn', 'funct': self.drop}
                ),
            ]

        super().__init__(app, prevView)
        

        self.streaming = False
        self.numBtnX = self.cax
        self.numBtnY = self.cay
        self.resetVectors()
        self.drawPots = False
        self.drawXY = False
        
        self.tests = 0
        
        self.startGraph()

        self.lastDataT = t.time()
        self.dataInt = 0.1
        self.inVals = 0
        self.tr = 0
        self.ta = 0
        
        self.initPreTestInfoLayout()
        
        self.inPrRect = rl.RectLabel(app = self.app,
                                     pos = (self.cax,  self.cay),
                                     dim = (70*d.px, 70*d.py),
                                     text = 'TESTING IN PROGRESS',
                                     font = self.app.viewTtlFont,
                                     fontCol = self.app.viewTtlFont,
                                     bcgCol = d.light_green
                                     )
        self.makeConfirmMsgs()
        

    def initPreTestInfoLayout(self):
        self.setItemFocusNum(0)
        self.setPostItemFocusNum(0)
        self.cols = [self.cax - 20*d.px, self.cax + 20*d.px]
        
        self.items = []
        self.postItems = []

        self.items.append(vb.ViewBtn(app = self.app,
                                    pos = (self.cols[0], self.cay - 20 * d.py + 20 * 0 * d.py),
                                    dim = (25*d.px, 18*d.py),
                                    label = 'FOLDER',
                                    value = self.app.getSetting(d.TEST_FOLDER),
                                    funct = self.toTestFolderSetting, 
                                    focus = True
                          )
        
        self.items.append(self.NoteListWrapper(self.app,self.disp,{'x':self.cols[1],'y':self.cay-10*d.py, 'xdim':20*d.px, 'ydim': 15*d.py}, listName = 'postTestNotes', focus =False, metaData = {'funct': self.toNoteSetting}))
        
        self.items.append(vb.ViewBtn(app = self.app,
                                    pos = (self.cols[0], self.cay - 20 * d.py + 20 * 1 * d.py),
                                    dim = (25*d.px, 18*d.py),
                                    label = 'PLOT #',
                                    value = self.app.getSetting(d.TEST_PLOT),
                                    funct = self.toPlotSetting,
                                    focus = True
                          )
        self.items.append(self.NoteListWrapper(self.app,self.disp,{'x':self.cols[1],'y':self.cay+20*d.py, 'xdim':20*d.px, 'ydim': 15*d.py}, listName = 'preTestNotes', focus =False, metaData = {'funct': self.toNoteSetting}))
        
        self.items.append(vb.ViewBtn(app = self.app,
                                    pos = (self.cols[0], self.cay - 20 * d.py + 20 * 2 * d.py),
                                    dim = (25*d.px, 18*d.py),
                                    label = 'HEIGHT',
                                    value = self.app.getSetting(d.TEST_HEIGHT),
                                    funct = self.toHeightSetting},
                                    focus = True
                          )
                
        self.postItems.append(nl.NoteList(self.app, self.disp,{'x':self.cax-28*d.px,'y':self.cay, 'xdim':20*d.px, 'ydim': 25*d.py}, listName = 'postTestNotes', hasFocus = True))


        self.postItems.append(vb.ViewBtn(app = self.app,
                                    pos = (self.cax-10*d.px, self.cay + 40 * d.py),
                                    dim = (15 * d.px, 10*d.py),
                                    label = 'Load',
                                    value = 'F',
                                    funct = self.switchLoadMode},
                                    focus = False
                          )

        self.postItems.append(vb.ViewBtn(app = self.app,
                                    pos = (self.cax+10*d.px, self.cay + 40 * d.py),
                                    dim = (15 * d.px, 10*d.py),
                                    label = 'Rot.',
                                    value = 'IMU',
                                    funct = self.switchRotMode},
                                    focus = False
                          )        
        
    def makeConfirmMsgs(self):
        #test folder
        self.pushMsg(msg.Message(self.app, self, self.disp,
                                    'Confirm/edit test folder.',
                                    'Current test folder: ' + self.app.getSetting(d.TEST_FOLDER),
                                    btnDefs = (
                                        {'label': 'CONFIRM', 'id': 'yesBtn', 'funct': self.popMsg},
                                        {'label': 'EDIT', 'id': 'yesBtn', 'funct': (self.popMsg, self.toTestFolderSetting)},
                                        {},
                                        {}
                                    )
                                    )
                         )
        #plot number
        self.pushMsg(msg.Message(self.app, self, self.disp,
                                    'Confirm/edit plot number.',
                                    'Current plot number: ' + str(self.app.getSetting(d.TEST_PLOT)),
                                    btnDefs = (
                                        {'label': 'CONFIRM', 'id': 'yesBtn', 'funct': self.popMsg},
                                        {'label': 'EDIT', 'id': 'yesBtn', 'funct': (self.popMsg, self.toPlotSetting)},
                                        {},
                                        {}
                                    )
                                    )
                         )
        
        #test height
        self.pushMsg(msg.Message(self.app, self, self.disp,
                                    'Confirm/edit test height.',
                                    'Current test height: ' + str(self.app.getSetting(d.TEST_HEIGHT)) + 'cm',
                                    btnDefs = (
                                        {'label': 'CONFIRM', 'id': 'yesBtn', 'funct': self.popMsg},
                                        {'label': 'EDIT', 'id': 'yesBtn', 'funct': (self.popMsg, self.toHeightSetting)},
                                        {},
                                        {}
                                    )
                                    )
                         )
        
        #plot preTestNotes
        preTestNotes = self.app.getSetting(d.PRE_TEST_NOTES)
        self.pushMsg(msg.Message(self.app, self, self.disp,
                                    'Confirm/edit pre-test notes.',
                                    'Current pre-test notes: ' + ', '.join(preTestNotes),
                                    btnDefs = (
                                        {'label': 'CONFIRM', 'id': 'yesBtn', 'funct': self.popMsg},
                                        {'label': 'EDIT', 'id': 'yesBtn', 'funct': (self.popMsg, self.toNoteSetting)},
                                        {},
                                        {}
                                    )
                                    )
                         )
        
        
    def setBreakHeight(self):
        self.app.setView(kbv.KeyboardView(self.app, self,
                                      d.NUM,
                                      'Break Height',
                                      'breakHeight',
                                      suffix = 'cm'
                                      ))
        
    def saveTest(self):
        dataMatrix = []
        dataMatrix.append(['PLOT',self.app.getSetting(d.TEST_PLOT), 'SENSOR','A','B','UNIT'])
        dataMatrix.append(['HEIGHT',self.app.getSetting(d.TEST_HEIGHT), d.DS_LOAD_X]+ list(self.getABUnit(d.DS_LOAD_X)))

        dataMatrix.append(['TEMPERATURE', self.app.getEnvData(d.TEMPERATURE), d.DS_LOAD_Y]+ list(self.getABUnit(d.DS_LOAD_Y)))
        dataMatrix.append(['HUMIDITY', self.app.getEnvData(d.HUMIDITY), d.DS_IMU]+ list(self.getABUnit(d.DS_IMU)))
        
        gpsData = self.app.getEnvData(d.LOCATION)
        
        if gpsData != hd.NO_GPS:
            [lat, lon] = gpsData.split('|')
            dataMatrix.append(['LATITUDE',lat, d.DS_POT]+ list(self.getABUnit(d.DS_POT)))
            dataMatrix.append(['LONGITUDE',lon, d.DS_HUM]+ list(self.getABUnit(d.DS_HUM)))
        else:
            dataMatrix.append(['LATITUDE',hd.NO_GPS, d.DS_POT]+ list(self.getABUnit(d.DS_POT)))
            dataMatrix.append(['LONGITUDE',hd.NO_GPS, d.DS_HUM]+ list(self.getABUnit(d.DS_HUM)))

        preNotes = self.app.getSetting(d.PRE_TEST_NOTES)
        for i in range(d.MAX_NOTES):
            #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            toAppend = ['PRE_TEST_NOTE_' + str(i+1), preNotes[i] if i < len(preNotes) else '']
            #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            if i ==0:
                toAppend += [d.DS_TEMP] + list(self.getABUnit(d.DS_TEMP))
                
            if self.breakHeight is not None:
                if i == 2:
                    toAppend += ['BREAK_HEIGHT', self.breakHeight]    

            dataMatrix.append(toAppend)
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        postNotes = self.postItems[0].getSelected()##self.noteList.getSelected()
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        for i in range(d.MAX_NOTES):
            #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            dataMatrix.append(['POST_TEST_NOTE_' + str(i+1), postNotes[i] if i< len(postNotes) else ''])
            #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%        
        max_len = len(self.times)
        
        print('self.anglePots', len(self.anglePots))
        print('self.angleImus', len(self.angleImus))
        print('self.loadsX', len(self.loadsX))
        print('self.loadsY', len(self.loadsY))
        print('self.times', len(self.times))
        
        
        
        if os.path.exists(d.USB_DATA_PATH):
            #usb is plugged in
            if not os.path.exists(d.USB_DATA_PATH + d.TESTS_DIR):
                #the tests folder does not exist ont he usb
                os.makedirs(d.USB_DATA_PATH + d.TESTS_DIR)
            TEST_FOLDERS_PATH = d.USB_DATA_PATH + d.TESTS_DIR
        else:
            if not os.path.exists(d.RASPI_DATA_PATH + d.TESTS_DIR):
                os.makedirs(d.RASPI_DATA_PATH + d.TESTS_DIR)
            TEST_FOLDERS_PATH = d.RASPI_DATA_PATH + d.TESTS_DIR
                
        fileName = self.app.getEnvData(d.TIME)
        folderPath = TEST_FOLDERS_PATH + '/' + self.app.getSetting(d.TEST_FOLDER)
        writePath =  folderPath + '/' + fileName
        if not os.path.isdir(folderPath):
            os.makedirs(folderPath)
        if os.path.exists(writePath + '.csv'):
            i = 2
            while os.path.exists(writePath +'(' + str(i) + ').csv'):
                i+=1
            writePath = writePath + '(' + str(i) + ')'
        with open(writePath + '.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for row in dataMatrix:
                writer.writerow(row)
            writer.writerow(['ANGLE_POT', 'ANGLE_IMU', 'LOAD_X', 'LOAD_Y', 'TIME'])
            for i in range(max_len):
            #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                writer.writerow([self.anglePots[i], self.angleImus[i], self.loadsX[i], self.loadsY[i], self.times[i]])
            #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            print('written file to: ' + writePath + '.csv')
    def padArray(self, arr, max_len):
        for i in range(max_len):
            if i >len(arr)-1:
                arr.append('')
    def selectBtn(self):
#         print('MODE:', self.mode, self.itemFocusNum, self.postItemFocusNum)
        if self.focusNum == preTest:
            self.items[self.itemFocusNum].funct()
        elif self.focusNum == postTest:
            if self.postItemFocusNum ==0:
                self.postItems[self.postItemFocusNum].selectCurrent()
            else:
                self.postItems[self.postItemFocusNum].funct()

    def setItemFocusNum(self, num):
        self.itemFocusNum = num

    def setItemFocus(self, num):
        self.items[self.itemFocusNum].setFocus(False)
        self.itemFocusNum = num
        self.items[self.itemFocusNum].setFocus(True)

    def setPostItemFocusNum(self, num):
        self.postItemFocusNum = num
        
    def setPostItemFocus(self, num):
        self.postItems[self.postItemFocusNum].setFocus(False)
        self.postItemFocusNum = num
        self.postItems[self.postItemFocusNum].setFocus(True)            

    def edit(self):
        self.items[self.itemFocusNum].funct()
    def toTestFiles(self):
        from views import pastTestsView as ptv
        print('go to past tests')
        self.app.setView(ptv.PastTestsView(self.app, self))
        
    #     self.focusItem.
    def toNoteSetting(self):
        from views import notesSettingView as nsv
        print('go to note setting')
        self.app.setView(nsv.NotesSettingView(self.app, self))


    def toTestFolderSetting(self):
        self.app.setView(kbv.KeyboardView(self.app, self,
                                      d.WORD,
                                      'Test folder',
                                      'testFolder',
                                      self.app.getSetting(d.TEST_FOLDER)
                                      ))
        
    def keyboardReturn(self, key, value, status = 1):
        if key == 'testFolder':
            self.app.saveSetting(d.TEST_FOLDER, value)
            self.initPreTestInfoLayout()
        elif key == 'breakHeight':
            self.breakHeight = float(value)

    def toPlotSetting(self):
        from views import plotSettingView as psv
        print('go to plot setting')
        self.app.setView(psv.PlotSettingView(self.app, self))

    def toHeightSetting(self):
        from views import heightSettingView as hv
        print('go to height setting')
        self.app.setView(hv.HeightView(self.app, self))

    def bringIfConfirmMsg(self):
        if not self.tests % self.app.getSetting(d.DATA_CONFIRM_FREQ):
            self.makeConfirmMsgs()
    
    def resetVectors(self):
        self.testData = np.array([])
        self.times = np.array([])
        self.loadsX = np.array([])
        self.loadsY = np.array([])
        self.loads = np.array([])
        self.anglePots = np.array([])
        self.angleImus = np.array([])
        self.breakHeight = None
    def startTest(self):
#         self.startDataIn = t.time()
        #self.focusNum = 1
        #self.raspTimes = []
        self.app.hd.getAll()
        self.app.streaming = True
        self.focusNum = inTest
        self.initButArea()
        self.app.hd.startStream()
    #overridden
    def convertedVector(self, vector, dataType):
        (a, b) = self.getAB(dataType)
        return (vector-b)/a
        
    def stopTest(self):
        #self.focusNum = 2
#         self.stopDataIn = t.time()
        self.app.streaming = False
        self.app.hd.stopStream()
        
        self.tests += 1
        
        self.focusNum = postTest
#         self.app.hd.getAll()
        self.initButArea()
        if self.times.size > 0:
            self.times -= self.times[0]
        
        
        ####convert data
        self.loadsX = self.convertedVector(self.loadsX, d.DS_LOAD_X)
        self.loadsY = self.convertedVector(self.loadsY, d.DS_LOAD_Y)
        self.anglePots = self.convertedVector(self.anglePots, d.DS_POT)
        self.angleImus = self.convertedVector(self.angleImus, d.DS_IMU)

        ####
        self.loads = np.sqrt(self.loadsX**2 + self.loadsY**2)
        
        
#         self.madeUpData()
        print('self.anglePots', len(self.anglePots))
        print('self.angleImus', len(self.angleImus))
        print('self.loadsX', len(self.loadsX))
        print('self.loadsY', len(self.loadsY))
        print('self.times', len(self.times))
        
        self.redrawGraph()
    def madeUpData(self):
        self.anglePots = np.arange(6, 26, 1)
        self.angleImus = self.anglePots
        self.loadsX = np.array([0,4,5,7,6,
                                9,14,17,11,23,
                                27,33,32,30,28,
                                25,20,15,10,5])
        self.loadsY = self.loadsX
        self.loads = self.loadsX##np.sqrt(self.loadsX**2 + self.loadsY**2)

    def redrawGraph(self, highlights = np.array([]), annotations = []):
                        
        with self.app.hd.threadLock:
            if not len(self.times):
                self.graph.clear()
                return
            
            if self.drawPots:
                angleUnit = ' (POT.)' + '[' + ((self.getABUnit(d.DS_POT))[-1])+']'
                angles = self.anglePots                            
            else:
                angleUnit = ' (IMU)' + '[' + ((self.getABUnit(d.DS_IMU))[-1])+']'
                angles = self.angleImus                            
            if self.drawXY:
                loadUnit = ' X: [' + ((self.getABUnit(d.DS_LOAD_X))[-1]) + '], Y: [' + ((self.getABUnit(d.DS_LOAD_Y))[-1]) +']'
                loads1 = self.loadsX
                loads2 = self.loadsY
                highlights = np.array([])
                
            else:
                loadUnit = ' F: [' + ((self.getABUnit(d.DS_LOAD_X))[-1]) + ']'
                loads1 = self.loads                                  
                loads2 = np.array([])
                                                             
            annotations = []
            #INDEX OUT OF BOUNDS %%%%%%%%%%%%%%%%%%%%
            if angles[0] > self.app.getSetting(d.MAX_START_ANGLE):
            #INDEX OUT OF BOUNDS %%%%%%%%%%%%%%%%%%%%
                annotations.append({'text':'SA '+ str("%0.1f" % angles[0])+ '>' + str(self.app.getSetting(d.MAX_START_ANGLE)),
                                    'index': 0,
                                    'ptx': angles[0],
                                    'pty': loads1[0],
                                    'xpos':1,
                                    'ypos': 0,
                                    'ha': 'right',
                                    'va': 'bottom',
                                    'bcg_col': 'red'})
            
#             (trueMaxInd, highlights) = pp.checkValidity(loads1)
#             if trueMaxInd != -1:
#                 annotations.append({'text':'ML (' + str("%0.1f" % loads1[trueMaxInd]) + ')',
#                     'index': trueMaxInd,
#                     'ptx': angles[trueMaxInd],
#                     'pty': loads1[trueMaxInd],                  
#                     'xpos': 0,
#                     'ypos': 1,
#                     'ha': 'left',
#                     'va': 'top',
#                     'bcg_col': 'green'})
# 
#             if self.drawXY:
#                 
#                 (trueMaxInd, hls) = pp.checkValidity(loads2)
#                                 
#                 if trueMaxInd != -1:
#                     annotations.append({'text':'MLY (' + str("%0.1f" % loads2[trueMaxInd]) + ')',
#                         'index': trueMaxInd,
#                         'ptx': angles[trueMaxInd],
#                         'pty': loads2[trueMaxInd],                     
#                         'xpos': 1,
#                         'ypos': 1,
#                         'ha': 'right',
#                         'va': 'top',
#                         'bcg_col': 'gray'})

            self.graph.updatePlot(
                x = angles,
                y1 = loads1,
                y2 = loads2,
                xlabel = 'ROT.' + angleUnit,
                ylabel = 'LOAD' + loadUnit,
                highlights = highlights,
                annotations = annotations                                              
            )
    def switchLoadMode(self):
        self.drawXY = not self.drawXY
        self.postItems[1].setValue('XY' if self.drawXY else 'F')
        self.postItems[1].setTxt()        
        self.redrawGraph()
    def switchRotMode(self):
        self.drawPots = not self.drawPots
        self.postItems[2].setValue('Pot.'if self.drawPots else 'IMU')
        self.postItems[2].setTxt()        
        self.redrawGraph()
    
    def save(self):
        self.saveTest()
        self.drop()
    def drop(self):
        self.resetVectors()
        self.focusNum = preTest
        self.initButArea()
        self.bringIfConfirmMsg()

    def back(self):
        if self.app.streaming:
            self.app.streaming = False
            self.app.hd.stopStream()
        from views import mainView as mv
        self.app.setView(self.prevView)

    def simulateDataIn(self):
        self.fullStreamDataIn(ri(0,100), ri(0,200), ri(0,100), ri(0,100), ri(0,100))
        self.lastDataT = t.time()
    def startGraph(self):
        self.graph = g.Graph(self.disp, {'x':self.cax+10*d.px, 'y':self.cay-2*d.py, 'xdim': 55, 'ydim':73})
    def displayView(self):
        self.butArea.display()
        if self.focusNum == preTest:
            for item in self.items:
                item.display()
        elif self.focusNum == inTest:
            self.inPrRect.display()
#             self.simulateDataIn()
        elif self.focusNum == postTest:
            self.graph.display()
            for item in self.postItems:
                item.display()
    def upArrowPress(self):
        if self.focusNum == preTest:
            if (self.itemFocusNum>=2):
                self.setItemFocus(self.itemFocusNum-2)
        elif self.focusNum == postTest:
            self.postItems[self.postItemFocusNum].upArrowPress()
    def downArrowPress(self):
        if self.focusNum == preTest:
            if (self.itemFocusNum<len(self.items)-2):
                self.setItemFocus(self.itemFocusNum+2)
        elif self.focusNum == postTest:
            self.postItems[self.postItemFocusNum].downArrowPress()
            
    def leftArrowPress(self):
        if self.focusNum == preTest:
            if (self.itemFocusNum>0):
                self.setItemFocus(self.itemFocusNum-1)
        elif self.focusNum == postTest:
            self.setPostItemFocus((self.postItemFocusNum-1)%3)
            pass

    def rightArrowPress(self):
        if self.focusNum == preTest:
            if (self.itemFocusNum<len(self.items)-1):
                self.setItemFocus(self.itemFocusNum+1)                
            else:
                self.leftArrowPress()
        elif self.focusNum == postTest:
            self.setPostItemFocus((self.postItemFocusNum+1)%3)
            pass

    def anglePotIn(self, value):
        if self.app.streaming:
            self.anglePots = np.append(self.anglePots, float(value))
        else:
            self.app.hd.stopStream()
    def angleImuIn(self, value):
        if self.app.streaming:

            self.angleImus = np.append(self.angleImus, float(value))
        else:
            self.app.hd.stopStream()

    def forceXIn(self, value):
        if self.app.streaming:

            self.loadsX = np.append(self.loadsX, float(value))
        else:
            self.app.hd.stopStream()

    def forceYIn(self, value):
        if self.app.streaming:

            self.loadsY = np.append(self.loadsY, float(value))
        else:
            self.app.hd.stopStream()

    def millisIn(self, value):
        if self.app.streaming:
            self.times = np.append(self.times, float(value))
        else:
            self.app.hd.stopStream()
        print('raspi: ' + str(int((t.time() - self.tr)*1000)), 'arduino: ' + str(float(value) - self.ta))
        self.tr = t.time()
        self.ta = float(value)
    def fullStreamDataIn(self, anglePot, angleImu, forceValueX, forceValueY, timeValue):
        pass
        #print('delta t', t.time() - self.lastDataIn, len(self.angles), len(self.loads), len(self.times))
        #self.raspTimes.append(t.time())
#         self.loadsX = np.append(self.loadsX, float(forceValueX))
#         self.loadsY = np.append(self.loadsY, float(forceValueY))
#         self.anglePots = np.append(self.anglePots, float(anglePot))
#         self.angleImus = np.append(self.angleImus, float(angleImu))
#         self.times = np.append(self.times, float(timeValue))
    def focusOn(self):
        self.initPreTestInfoLayout()
        super().focusOn()
        
#     class SettingBtn:
#         def __init__(self, app,geoData, metaData, focus, dim = (25*d.px, 18*d.py)):
#             self.app = app
#             self.disp = self.app.disp
#             self.x = geoData['x']
#             self.y = geoData['y']
#             self.xdim = dim[0]
#             self.ydim = dim[1]
#             self.label = metaData['label']
#             self.value = metaData['value']
#             self.funct = metaData['funct']
#             
#             self.rl = rl.RectLabel(self.app,
#                                    (self.x, self.y),
#                                    (self.xdim, self.ydim),
#                                    self.getLabel(),
#                                    self.app.stnBtnFont,
#                                    self.app.font_col,
#                                    self.self.bcgCol
#                                    )
#             
#             
#             self.setFocus(focus)
# 
#         def setValue(self, value):
#             self.value = value
#             self.rl.setText(self.getLabel())
#         def setFocus(self, focus):
#             self.focus = focus
#             self.setBcgCol()
#         def getLabel(self):
#             return self.label+ ': ' + str(self.value) + ('mm' if self.label == 'Height' else '')
#         def setBcgCol(self):
#             self.bcgCol = d.textView_highlight_col if self.focus else self.app.textView_col
#             self.rl.setBcgCol(self.bcgCol)
#         def display(self):
#             self.rl.display()
#         def upArrowPress(self):
#             pass
#         def downArrowPress(self):
#             pass
    class NoteListWrapper:
        def __init__(self, app, disp, geoData, list = None, listName='', focus= False, metaData={}):
            self.app = app
            self.x = geoData['x']
            self.y = geoData['y']
            self.xdim = 1.2*geoData['xdim']
            self.ydim = 1.5*geoData['ydim']

            self.focus = focus
            self.disp = disp
            self.funct = metaData['funct']

            self.nl = nl.NoteList(app, disp, geoData, list, listName, False)

            self.setFocus(focus)

        def setFocus(self, focus):
            self.focus = focus
            self.setBcgCol()
        def setBcgCol(self):
            self.bcgCol = d.textView_highlight_col if self.focus else d.darkenColor(self.app.textView_col)
        def display(self):
            pg.draw.rect(self.disp, self.bcgCol, (self.x - self.xdim / 2, self.y - self.ydim / 2, self.xdim, self.ydim))
            self.nl.display()
