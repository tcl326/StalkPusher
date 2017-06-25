#!/usr/bin/env python3
if __name__ == '__main__':
    import os, sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pygame as pg
from hardware import hdInterface2 as hi
from views import mainView as mv
from main import defs as d
#from items import graph
from views import testingView as tv
from views import settingsView as sv
from views import liveFeedView as lfv
import time as t
import threading as thr
import sys
import os


class CropDevMain:
    def __init__(self):
        self.run()
    def run(self):
        self.running = False
        self.view = None
        self.readSettings()

        self.envData = {}
        self.msgStack = []
        self.lastIn = 0
        self.threadLock = thr.Lock()
        self.initHDInput()
        self.initBtnInput()
        self.initPG()
        self.loop()
    def pushMsg2Stack(self, msg):
        self.msgStack.append(msg)
        
    def serialConnFail(self):
        if self.view is not None:
            self.view.serialConnFail()
        self.pushMsg2Stack('serialConnFail')


    def initPG(self):
        if d.FULLSCREEN:
            self.disp = pg.display.set_mode((int(d.width), int(d.height)), pg.FULLSCREEN)
        else:
             self.disp = pg.display.set_mode((int(d.width), int(d.height)))          
        pg.mouse.set_visible(False)
        self.clock = pg.time.Clock()
#         self.bcgCol = list(d.bcg_col)
        self.blitScreen = True
        self.createFonts()
        self.createViews()
        
        self.setView(self.mainView)
        self.view.getAll()
        self.btnInput.resetBtnPresses()
        self.running = True
    def createFonts(self):
        self.btnFont = pg.font.SysFont('Arial', d.BTN_FS, True)
        self.viewTtlFont = pg.font.SysFont('Arial', d.VIEW_TTL_FS, True)
        self.nlFont = pg.font.SysFont('Arial', d.NL_FS, True)
        self.lvVbFONT = pg.font.SysFont('Arial', d.LV_VB_FS, True)

        self.stnBtnFont = pg.font.SysFont('Arial', d.STN_BTN_FS, True)
        self.msgTtlFont = pg.font.SysFont('Arial', d.MSG_TTL_FS, True)
        self.msgBdFont = pg.font.SysFont('Arial', d.MSG_BD_FS, True)
        self.kbKeyFont = pg.font.SysFont('Arial', d.KB_KEY_FS, True)
        self.numKeyFont = pg.font.SysFont('Arial', d.NK_FS, True)
        
    def updateScreen(self):
#         if not self.blitScreen:
#         print('update screen')
        self.blitScreen = True       
    def createViews(self):

        self.mainView = mv.MainView(self)
        self.settingsView = sv.SettingsView(self, self.mainView)
        self.testingView = tv.TestingView(self, self.mainView)
        self.liveFeedView = lfv.LiveFeedView(self, self.mainView)

    def initHDInput(self):
        self.streaming = False
        self.hd = hi.HardWare(self)
    def initBtnInput(self):
        from hardware import btnInput2 as bi
        self.btnMap = [self.btn1Press, self.btn2Press, self.btn3Press, self.btn4Press, self.upArrowPress, self.leftArrowPress, self.rightArrowPress, self.downArrowPress]
        self.btnInput = bi.BtnInput(
                                    {   'btn1Press': self.btn1Press,
                                        'btn2Press': self.btn2Press,
                                        'btn3Press': self.btn3Press,
                                        'btn4Press': self.btn4Press,
                                        'upArrowPress': self.upArrowPress,
                                        'leftArrowPress': self.leftArrowPress,
                                        'rightArrowPress': self.rightArrowPress,
                                        'downArrowPress': self.downArrowPress
                                     }
        )
    def readSettings(self):
        fileData = d.readSettings()
        self.data = {}
        for DATA_STRING in d.dataStrings:
            try:
                self.data[DATA_STRING] = fileData[DATA_STRING]
            except:
                self.data[DATA_STRING] = 'N/A'
                
        self.bcg_col = tuple(self.data[d.COLORS]['bcg_col'])
        self.textView_col = tuple(self.data[d.COLORS]['textView_col'])
        self.font_col = tuple(self.data[d.COLORS]['font_col'])        
        
    def getSetting(self, setting):
        return self.data[setting]

    def saveSetting(self, setting, value):
        self.data[setting] = value
        d.saveSetting(setting, value)
    def getEnvData(self, type):
        if type in self.envData:
            return self.envData[type]
        else:
            return 'NA'
    def saveEnvData(self, type, value):
        self.envData[type] = value

    def loop(self):
        while self.running:
#             try:
#             self.view.display()
            
            self.btnInput.checkInput()
            self.checkBtns()
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_1:
                        self.btn1Press()
                    if event.key == pg.K_q:
                        self.btn2Press()
                    if event.key == pg.K_a:
                        self.btn3Press()
                    if event.key == pg.K_z:
                        self.btn4Press()
                    if event.key == pg.K_UP:
                        self.upArrowPress()
                    if event.key == pg.K_LEFT:
                        self.leftArrowPress()
                    if event.key == pg.K_RIGHT:
                        self.rightArrowPress()
                    if event.key == pg.K_DOWN:
                        self.downArrowPress()
                    if event.key == pg.K_p:
                        self.takeScreenshot()
                if event.type == pg.QUIT:
                    self.exit()
            if self.blitScreen:
#                 print('display.update() start')

                self.disp.fill(self.bcg_col)
                self.view.display()
                pg.display.update()
                self.blitScreen = False
#                 print('display.update() end')

            self.clock.tick(60)
            ##########################   TO BE UNCOMMENTED
#             except Exception as e:
#                 if self.view is not None:
#                     from items import message as ms
#                     self.view.pushMsg(ms.Message(self, self.view, self.disp,
#                                             'Software encountered an issue.',
#                                             'Error: ' + str(e),
#                                             btnDefs = (
#                                                 {'label': 'OK', 'id': 'yesBtn', 'funct': self.view.popMsg},
#                                                 {},
#                                                 {},
#                                                 {}
#                                             )
#                                             )
#                                  )
#                        
#                 else:
#                     print('Software encountered an issue. Error: ' + str(e))
#                     cropDevErrorLogFile.write(str(e))
            ##########################
    def checkBtns(self):
        btnPr = self.btnInput.btnPresses
        for i in range(len(btnPr)):
            if btnPr[i]:
                self.btnMap[i]()
                btnPr[i] = False

                break
            
    def setView(self, view):
        if self.view is not None:
            self.view.focusOut()
        self.view = view
        self.view.focusOn()
    def setViewWithArg(self, view, arg):
        self.view = view
        self.view.focusOnWithArg(arg)
    def btn1Press(self):
        print('Button 1 Press')
        self.view.btn1Press()
    def btn2Press(self):
        print('Button 2 Press')
        self.view.btn2Press()
    def btn3Press(self):
        print('Button 3 Press')
        self.view.btn3Press()
    def btn4Press(self):
        print('Button 4 Press')
        self.view.btn4Press()
    def upArrowPress(self):
        print('UP')
        self.view.upArrowPress()
    def downArrowPress(self):
        print('DOWN')
        self.view.downArrowPress()
    def leftArrowPress(self):
        print('LEFT')
        self.view.leftArrowPress()
    def rightArrowPress(self):
        print('RIGHT')
        self.view.rightArrowPress()
    
    
    def exit(self):
        self.running = False
#         import subprocess
#         command = "sudo python3 /home/pi/Desktop/StalkPusher/gui/main/cropDev.py &"
#         process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
#         
#         output = process.communicate()[0]
#         quit()
#        
# 
#         print(output)
        
    def restartSoftware(self):
        self.hd.closeConnection()
        """Restarts the current program.
        Note: this function does not return. Any cleanup action (like
        saving data) must be done before calling this function."""
        python = sys.executable
        os.execl(python, python, * sys.argv)


    def restartPi(self):
        self.hd.closeConnection()
        command = "/usr/bin/sudo /sbin/shutdown -r now"
        import subprocess
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        output = process.communicate()[0]
        print(output)
    def shutdownPi(self):
        self.hd.closeConnection()
        command = "/usr/bin/sudo /sbin/shutdown -h now"
        import subprocess
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        output = process.communicate()[0]
        print(output)
    def takeScreenshot(self):
        PATH = '/home/pi/Pictures/CropDev'
        fileName = 'screenshot'
        writePath = PATH + '/' + fileName
        if not os.path.exists(PATH):
            #the tests folder does not exist ont he usb
            os.makedirs(PATH)
        
        if os.path.exists(writePath + '.jpg'):
            i = 2
            while os.path.exists(writePath + str(i) + '.jpg'):
                i+=1
            writePath = writePath + str(i)
       
        rect = pg.Rect(0, 0, d.width, d.height)
        sub = self.disp.subsurface(rect)
        pg.image.save(sub, writePath + '.jpg')

if __name__ == '__main__':
#     cropDevErrorLogFile = open('/home/pi/Desktop/cropDevErrorLogFile.txt', 'a+')
#     sys.stderr = cropDevErrorLogFile
    mw = CropDevMain()
    pg.quit()
    mw.hd.closeConnection()
    quit()
