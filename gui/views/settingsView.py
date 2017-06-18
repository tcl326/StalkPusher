'''
settingsView.py created by Witold on 2/1/2017 under the pygametrial project
'''
import pygame as pg
import defs as d
from views import view as v
from utils import text as txt
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
            {'label': 'SENSORS', 'funct': self.toSensorSettingView}
#             {'label': 'VOLUME', 'funct': self.toPendingSetting},
#             {'label': 'GPS', 'funct': self.toPendingSetting},
#             {'label': 'UPDATE', 'funct': self.toPendingSetting},
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
            self.stnBtns.append(self.SettingBtn(self.app, {'x': col, 'y': row}, self.stnBtnDefs[i],i == self.stnBtnFocusNum))
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
        
    def toCalibrationChoiceView  (self):
        from views import calibrationChoiceView as ccv
        self.app.setView(ccv.CalibrationChoiceView(self.app, self))
       
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

    class SettingBtn:
        def __init__(self, app,geoData, metaData, focus):
            self.app = app
            self.disp = self.app.disp
            self.x = geoData['x']
            self.y = geoData['y']
            self.xdim = 18*d.px
            self.ydim = 18*d.py
            self.label = metaData['label']
            self.funct = metaData['funct']
            self.setFocus(focus)
            self.txtDim = txt.findFontSize(self.label, 'Arial', self.xdim, self.ydim, 4*d.px)#int(4*d.px)
            self.setBcgCol()

            self.setFontCol()

            self.setFont()

            self.setTxt()

        def setFocus(self, focus):
            self.focus = focus
            self.setBcgCol()

        def setTxt(self):
            self.txt = self.font.render(self.label, True, self.fontCol)
        def setFont(self):
            self.font = pg.font.SysFont('Arial', self.txtDim, bold = True)
        def setBcgCol(self):
            self.bcgCol = d.textView_highlight_col if self.focus else self.app.textView_col
        def setFontCol(self):

            self.fontCol = self.app.font_col

        def display(self):
            # display rect
            pg.draw.rect(self.disp, self.bcgCol, (self.x - self.xdim / 2, self.y - self.ydim / 2, self.xdim, self.ydim))
            #display number
            self.disp.blit(self.txt, (self.txt.get_rect(center=(self.x, self.y))))
