'''
settingsView.py created by Witold on 2/1/2017 under the pygametrial project
'''
import pygame as pg
import defs as d
from views import view as v
from utils import text as txt
from items import message as msg
from items import viewBtn as vb
 
import os
class SettingsView(v.View):
    def __init__(self, app, prevView = None):
        self.btnDefs = [(
            {'label': 'SELECT', 'id': 'selectBtn', 'funct': self.select},
            {},
            {},
            {'label': 'BACK', 'id': 'bckBtn', 'funct': self.back}
        )]
        self.title = 'SETTINGS'
        super().__init__(app, prevView)

        self.stnBtnDefs = (
            {'label': 'HEIGHT', 'funct': self.toHeightSetting},
            {'label': 'PLOT', 'funct': self.toPlotSetting},
            {'label': 'NOTE', 'funct': self.toNoteSetting},
            {'label': 'COLORS', 'funct': self.toColorTesting},
            {'label': 'SENSORS', 'funct': self.toSensorSettingView},
#             {'label': 'VOLUME', 'funct': self.toPendingSetting},
#             {'label': 'GPS', 'funct': self.toPendingSetting},
            {'label': 'UPDATE', 'funct': self.checkUSB},
#             {'label': 'ABOUT', 'funct': self.toPendingSetting},
        )
        self.numStnBtnRow = 2
        self.numStnBtnCom = 3
        self.setStnFocusNum(0)
        self.stnBtnsCols = (self.cax - 24*d.px, self.cax, self.cax + 24*d.px)
        self.stnBtnsRows = (self.cay - 24*d.py, self.cay, self.cay + 24*d.py)
        self.addStnBtns()
    def setStnFocusNum(self, num):
        self.stnBtnFocusNum = num
    
    def addStnBtns(self):
        self.stnBtns = []
        for i in range(len(self.stnBtnDefs)):
            row = self.stnBtnsRows[i // 3]
            col = self.stnBtnsCols[i % 3]
            self.stnBtns.append(vb.ViewBtn(app = self.app,
                                           pos = (col, row),
                                           dim = (20*d.px, 18*d.py),
                                           label = self.stnBtnDefs[i]['label'],
                                           funct = self.stnBtnDefs[i]['funct'],
                                           focus =  i == self.stnBtnFocusNum),
                                )            
#             self.stnBtns.append(self.SettingBtn(self.app, {'x': col, 'y': row}, self.stnBtnDefs[i],i == self.stnBtnFocusNum))
    def displayView(self):
        for stnBtn in self.stnBtns:
            stnBtn.display()
    def select(self):
        self.stnBtns[self.stnBtnFocusNum].funct()
    def toHeightSetting(self):
        from views import heightSettingView as hv
        print('go to height setting')
        self.app.setView(hv.HeightView(self.app, self))

    def toPlotSetting(self):
        from views import plotSettingView as psv
        print('go to plot setting')
        self.app.setView(psv.PlotSettingView(self.app, self))

    def toNoteSetting(self):
        from views import notesSettingView as nsv
        print('go to note setting')
        self.app.setView(nsv.NotesSettingView(self.app, self))
    def toColorTesting(self):
        from views import colorTestView as ctv
        self.app.setView(ctv.ColorTestView(self.app, self))
    def toSensorSettingView(self):
        from views import sensorSettingView as ssv
        self.app.setView(ssv.SensorSettingView(self.app, self))
        
    def toUpdateSetting(self):
        from views import updateView as uv
        self.app.setView(uv.UpdateView(self.app, self))
               
    def toPendingSetting(self):
        pass
    def back(self):
        from views import mainView as mv
        print('go back')
        self.app.setView(self.prevView)

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
            
#     class SettingBtn:
#         def __init__(self, app,geoData, metaData, focus):
#             self.app = app
#             self.disp = self.app.disp
#             self.x = geoData['x']
#             self.y = geoData['y']
#             self.xdim = 18*d.px
#             self.ydim = 18*d.py
#             self.label = metaData['label']
#             self.funct = metaData['funct']
#             self.setFocus(focus)
#             self.txtDim = int(3.8*d.px)
#             self.setBcgCol()
# 
#             self.setFontCol()
# 
#             self.setFont()
# 
#             self.setTxt()
# 
#         def setFocus(self, focus):
#             self.focus = focus
#             self.setBcgCol()
#             self.app.updateScreen()
#         def setTxt(self):
#             self.txt = self.font.render(self.label, True, self.fontCol)
#         def setFont(self):
#             self.font = pg.font.SysFont('Arial', self.txtDim, bold = True)
#         def setBcgCol(self):
#             self.bcgCol = d.textView_highlight_col if self.focus else self.app.textView_col
#         def setFontCol(self):
#             self.fontCol = self.app.font_col
# 
#         def display(self):
#             # display rect
#             pg.draw.rect(self.disp, self.bcgCol, (self.x - self.xdim / 2, self.y - self.ydim / 2, self.xdim, self.ydim))
#             #display number
#             self.disp.blit(self.txt, (self.txt.get_rect(center=(self.x, self.y))))

    """
    Update SUB Stick structure
    /
        /update
            updateData.json
            /cropDevice
                /main
                /utils
                /views
                /...
    updateConf.json contains following info:
    - new version
    - replace appData.json?
    - etc.
    """
    def checkUSB(self):
        validUpdate = False
        updatePath = d.USB_DATA_PATH+d.UPDATE_DIR
        print('u[date path: ', updatePath)
        print('checking if update path exists')

        if os.path.exists(updatePath):
            updateDataPath = os.path.join(updatePath, 'updateData.json')
            print('u[date data path: ', updateDataPath)
            print('update path exists')
            if os.path.isfile(updateDataPath):
                updateData = d.readSettingFromFile(updateDataPath)
                newVersion = updateData['version']
                validUpdate = True
                print('update data exists')

        if validUpdate:
            self.pushMsg(msg.Message(self.app, self, self.disp,
                                        'Valid update found.',
                                        'Current version: ' + self.app.getSetting(d.VERSION) + ' New version: ' + newVersion,
                                        btnDefs = (
                                            {'label': 'UPDATE', 'id': 'yesBtn', 'funct': (self.popMsg, self.updateSoftware)},
                                            {},
                                            {},
                                            {'label': 'CANCEL', 'id': 'yesBtn', 'funct': self.popMsg}
                                        )
                                        )
                             )
        else:
            #either no USB stick or incorrect folder structure
            self.pushMsg(msg.Message(self.app, self, self.disp,
                                        'No valid update.',
                                        'Insert USB stick with valid update',
                                        btnDefs = (
                                            {'label': 'RETRY', 'id': 'yesBtn', 'funct': (self.popMsg, self.checkUSB)},
                                            {},
                                            {},
                                            {'label': 'CANCEL', 'id': 'yesBtn', 'funct': self.popMsg}
                                        )
                                        )
                             )
            
    def updateSoftware(self):
        import subprocess
        updatePath = d.USB_DATA_PATH+d.UPDATE_DIR
        newSoftwarePath = os.path.join(updatePath, 'cropDevice')
        sampleFilePath = os.path.join(newSoftwarePath, 'sampleFile.txt')
        
        command = 'sudo cp ' + sampleFilePath + ' ' + d.MAINAPP_PATH
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        output = process.communicate()[0]
        
        self.pushMsg(msg.Message(self.app, self, self.disp,
                                    'Update succesful.',
                                    'Restart device to apply changes.',
                                    btnDefs = (
                                        {'label': 'RESTART', 'id': 'yesBtn', 'funct': (self.popMsg, self.app.restartPi)},
                                        {},
                                        {},
                                        {'label': 'LATER', 'id': 'yesBtn', 'funct': self.popMsg}
                                    )
                                    )
                         )
        
        
        

