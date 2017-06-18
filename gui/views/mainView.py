'''
Created on Jan 30, 2017

Main menu view (welcome screen)

@author: Witold
'''

import pygame as pg
import views.view as v
import defs as d
import time as t
from utils import text as txt
class MainView(v.View):
    def __init__(self, app):

        self.btnDefs = [(
            {'label': 'SETTINGS', 'id': 'stgsBtn', 'funct': self.goToSettings},
            {'label': 'TESTING', 'id': 'tstBtn', 'funct': self.goToTesting},
            {'label': 'LIVE FEED', 'id': 'snfBtn', 'funct': self.goToLiveFeed},
            {'label': 'EXIT', 'id': 'bckBtn', 'funct': self.exitBtn})
            ]

        self.stnBtnDefs = (
            {'label': 'TEMP', 'funct': self.getTemperature},
            {'label': 'HUM', 'funct': self.getHumidity},
            {'label': 'GEO', 'funct': self.getLocation},
            {'label': 'TIME', 'funct': self.getTime}
        )

        self.title = 'MAIN MENU'

        super().__init__(app)

        self.caTtlfont = pg.font.SysFont('Arial', 40, bold = True)
        self.caTtltxt = self.caTtlfont.render('CROP DEVICE ' + self.app.getSetting(d.VERSION), True, d.font_col_inv)

        self.numStnBtnRow = 2
        self.numStnBtnCom = 2
        self.setStnFocusNum(0)
        self.stnBtnsCols = (self.cax - 18*d.px, self.cax + 18*d.px)
        self.stnBtnsRows = (self.cay + 20*d.py, self.cay + 40*d.py)

        self.addStnBtns()
                
    def setStnFocusNum(self, num):
        self.stnBtnFocusNum = num
    def addStnBtns(self):
        self.stnBtns = []
        for i in range(len(self.stnBtnDefs)):
            row = self.stnBtnsRows[i // self.numStnBtnCom]
            col = self.stnBtnsCols[i % self.numStnBtnRow]
            self.stnBtns.append(self.SettingBtn(self.app, {'x': col, 'y': row}, self.stnBtnDefs[i],i == self.stnBtnFocusNum))
#         for stnBtn in self.stnBtns:
#             stnBtn.display()
    def select(self):
        self.app.hd.getAll()

    
    def displayView(self):
        #display title for context area
        self.disp.blit(self.caTtltxt, (self.caTtltxt.get_rect(center=(self.cax, self.cay))))
        for stnBtn in self.stnBtns:
            stnBtn.display()
        
    def goToLiveFeed(self):
        import views.testingView as tv
        print('view: go to live feed')
        self.app.setView(self.app.liveFeedView)
        self.app.liveFeedView.startQuerying()

    def goToTesting(self):
        import views.testingView as tv
        print('view: go to testing')
        self.app.setView(self.app.testingView)

    def goToSettings(self):
        import views.settingsView as sv
        print('going to settings')
        self.app.setView(self.app.settingsView)

    def upArrowPress(self):
        if (self.stnBtnFocusNum>=self.numStnBtnCom):
            self.stnBtns[self.stnBtnFocusNum].setFocus(False)
            self.stnBtnFocusNum-=self.numStnBtnCom
            self.stnBtns[self.stnBtnFocusNum].setFocus(True)

    def downArrowPress(self):
        if (self.stnBtnFocusNum<len(self.stnBtnDefs)-self.numStnBtnCom):
            self.stnBtns[self.stnBtnFocusNum].setFocus(False)
            self.stnBtnFocusNum+=self.numStnBtnCom
            self.stnBtns[self.stnBtnFocusNum].setFocus(True)

    def leftArrowPress(self):
        if (self.stnBtnFocusNum>0):
            self.stnBtns[self.stnBtnFocusNum].setFocus(False)
            self.stnBtnFocusNum-=1
            self.stnBtns[self.stnBtnFocusNum].setFocus(True)

    def rightArrowPress(self):
        if (self.stnBtnFocusNum<len(self.stnBtnDefs)-1):
            self.stnBtns[self.stnBtnFocusNum].setFocus(False)
            self.stnBtnFocusNum+=1
            self.stnBtns[self.stnBtnFocusNum].setFocus(True)

    def timeIn(self, year, month, day, hour, minute, second, millis):
        super().timeIn(year, month, day, hour, minute, second, millis)
        value = hour+':'+str(minute)+', '+ str(day)+'/'+str(month)+'/'+str(year) #':'+str(second)+'.'+str(millis)+
        next((x for x in self.stnBtns if x.label == 'TIME'), None).setValue(value)
    def locationIn(self, x, y):
        super().locationIn(x, y)
        next((x for x in self.stnBtns if x.label == 'GEO'), None).setDValue(x, y)
    def noGPS(self):
        super().noGPS()
        next((x for x in self.stnBtns if x.label == 'GEO'), None).setValue('No GPS')        
    def temperatureIn(self, value):
        super().temperatureIn(value)
        next((x for x in self.stnBtns if x.label == 'TEMP'), None).setValue(value)
    def humidityIn(self, value):
        super().humidityIn(value)
        next((x for x in self.stnBtns if x.label == 'HUM'), None).setValue(value)
#     def connectionEstablished(self):
#         print('main: established conn')
#         self.getAll()

    class SettingBtn:
        def __init__(self, app, geoData, metaData, focus):
            self.app = app
            self.disp = self.app.disp
            self.x = geoData['x']
            self.y = geoData['y']
            self.xdim = 25*d.px
            self.ydim = 18*d.py
            self.label = metaData['label']
            self.funct = metaData['funct']
            self.value = 'N/A'
            self.setFocus(focus)
            self.txtDim = int(2.5*d.px)
            self.setBcgCol()

            self.setFontCol()

            self.setFont()

            self.setTxt()

        def setValue(self, value):
            self.value = str(value)
            self.setFont()
            self.setTxt()
        def setDValue(self, value1, value2):
            self.value = str(value1)  +', ' + str(value2)
            self.setFont()
            self.setTxt()
        def setFocus(self, focus):
            self.focus = focus
            self.setBcgCol()
            self.app.updateScreen()

        def setTxt(self):
            #self.setFont()
            self.txt = self.font.render(self.label + ': ' +self.value, True, self.fontCol)
            self.app.updateScreen()
        def setFont(self):
            self.font = pg.font.SysFont('Arial', txt.findFontSize(self.label + ': ' +self.value, 'Arial', self.xdim, self.ydim, 4*d.px), bold = True)#self.txtDim
        def setBcgCol(self):

            self.bcgCol = d.textView_highlight_col if self.focus else self.app.textView_col
        def setFontCol(self):

            self.fontCol = self.app.font_col

        def display(self):
            # display rect
            pg.draw.rect(self.disp, self.bcgCol, (self.x - self.xdim / 2, self.y - self.ydim / 2, self.xdim, self.ydim))
            #display number
            self.disp.blit(self.txt, (self.txt.get_rect(center=(self.x, self.y))))
    def exitBtn(self):
        from items import message as ms
        self.pushMsg(ms.Message(self.app, self, self.disp,
                                'EXITING',
                                'Choose exit mode.',
                                btnDefs = (
                                    {'label': 'EXIT', 'id': 'exitBtn', 'funct': self.bringExitMsg},
                                    {'label': 'RESTART', 'id': 'restartBtn', 'funct': self.bringRestartMsg},
                                    {'label': 'SHUT\nDOWN', 'id': 'shutdownBtn', 'funct': self.bringShutdownMsg},
                                    {'label': 'CANCEL', 'id': 'cancelBtn', 'funct': self.popMsg}
                                )
                                )
                     )
    def bringShutdownMsg(self):
        from items import message as ms
        self.pushMsg(ms.Message(self.app, self, self.disp,
                                'SHUTTING DOWN DEVICE...',
                                'ARE YOU SURE?',
                                btnDefs = (
                                    {'label': 'YES', 'id': 'yesBtn', 'funct': self.app.shutdownPi},
                                    {'label': 'NO', 'id': 'noBtn', 'funct': self.popMsg},
                                    {},
                                    {}
                                )
                                )
                     )
    def bringExitMsg(self):
        from items import message as ms
        self.pushMsg(ms.Message(self.app, self, self.disp,
                                'EXITING SOFTWARE',
                                'ARE YOU SURE?',
                                btnDefs = (
                                    {'label': 'YES', 'id': 'yesBtn', 'funct': self.exit},
                                    {'label': 'NO', 'id': 'noBtn', 'funct': self.popMsg},
                                    {},
                                    {}
                                )
                                )
                     )
        
    def exit(self):
        self.app.exit()
