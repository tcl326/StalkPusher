from items import noteList as nl
import os
from views import view as v
from main import defs as d
from items import message as msg
from views import keyboardView as kbv

class EditSensorView(v.View):
    def __init__(self, app, sensorType, sensorName, prevView = None):
        self.title = 'EDIT ' + sensorName +' SENSOR'
        self.btnDefs = [
                (
                    {'label': 'SAVE', 'id': 'startBtn', 'funct': self.saveSensor},
                    {'label': 'EDIT', 'id': 'startBtn', 'funct': self.editField},
                    {},
                    {'label': 'CANCEL', 'id': 'bckBtn', 'funct': self.goBack}
                )
            ]
        super().__init__(app, prevView)
        self.sensorType = sensorType
        self.sensorName = sensorName
        self.sensorData = self.app.getSetting(d.SENSOR_BANK)[self.sensorType][self.sensorName]
        
        self.numBtnX = self.cax
        self.numBtnY = self.cay
        self.initLists()
        
    def initLists(self):
        self.nls = []
        
        self.nls.append(nl.NoteList(self.app, self.disp,{'x':self.cax-20*d.px,'y':self.cay, 'xdim':28*d.px, 'ydim': 50*d.py}, d.SENSOR_FIELDS, 'Data field', True))
        
        
        l = [self.sensorData[self.nls[0].getItem()]]
        
        self.nls.append(nl.NoteList(self.app, self.disp,{'x':self.cax+20*d.px,'y':self.cay, 'xdim':28*d.px, 'ydim': 50*d.py}, l, self.sensorData[self.nls[0].getItem()], False))
            
#         self.focus = 0
#         self.folderList[self.focus].setFocus(True)
    def editField(self):
        fieldType = self.nls[0].getItem()
        input = self.nls[1].getItem()
        if fieldType == d.SENSOR_A or fieldType == d.SENSOR_B:
            kbType = d.NUM
        else:
            kbType = d.WORD
            
        self.app.setView(kbv.KeyboardView(self.app, self,
                         kbType,
                         fieldType,
                         fieldType,
                         input)
                         )
    def keyboardReturn(self, key, value, status = 1):
        if key == d.SENSOR_A or key == d.SENSOR_B:
            try:
                value = float(value)        
                self.sensorData[key] = value
                self.initLists()
            except:
                self.pushMsg(msg.Message(self.app, self, self.disp,
                                        'Invalid data',
                                        'Input mst b a valid numerical value. Retry',
                                        btnDefs = (
                                            {'label': 'OK', 'id': 'yesBtn', 'funct': self.popMsg},
                                            {'label': 'RETRY', 'id': 'yesBtn', 'funct': self.popMsg},
                                            {},
                                            {}
                                        )
                                        )
                             )
                
    def saveSensor(self):
        #make it more efficient - access only needed data fields
        #I assume that sensorData is being changed every time a field is changed
        allSensors = self.app.getSetting(d.SENSOR_BANK)
        allSensors[self.sensorType][self.sensorName] = self.sensorData
        self.app.saveSetting(d.SENSOR_BANK, allSensors)
        self.goBack()
        
    def replaceList(self, fieldType):
        l = [self.sensorData[fieldType]]
        self.nls[1] = (nl.NoteList(self.app, self.disp,{'x':self.cax+20*d.px,'y':self.cay, 'xdim':28*d.px, 'ydim': 50*d.py}, l, self.sensorName + ' sensors', False))
        
        
    def getAllSensors(self, sensorType):
        return list(self.app.getSetting(d.SENSOR_BANK)[sensorType])
        
    def upArrowPress(self):
        self.nls[self.focusNum].upArrowPress()
        if self.focusNum ==0:
            self.replaceList(self.nls[0].getItem())
    def downArrowPress(self):
        self.nls[self.focusNum].downArrowPress()
        if self.focusNum ==0:
            self.replaceList(self.nls[0].getItem())
#     def leftArrowPress(self):
# 
#         self.nls[self.focusNum].setFocus(False)
#         self.focusNum = not self.focusNum
#         self.nls[self.focusNum].setFocus(True)
#         self.initButArea()
# 
#     def rightArrowPress(self):
# 
#         self.nls[self.focusNum].setFocus(False)
#         self.focusNum = not self.focusNum
#         self.nls[self.focusNum].setFocus(True)
#         self.initButArea()

    def displayView(self):
        for fl in self.nls:
            fl.display()