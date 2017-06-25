from items import noteList as nl
import os
from views import view as v
from main import defs as d
class PastTestsView(v.View):
    def __init__(self, app, prevView = None):
        self.title = 'Test Files'
        self.btnDefs = [
                (
                    {},#'label': 'SELECT', 'id': 'startBtn', 'funct': self.selectFolder
                    {},
                    {},
                    {'label': 'BACK', 'id': 'bckBtn', 'funct': self.goBack}
                ),
                (
                    {'label': 'VIEW', 'id': 'startBtn', 'funct': self.selectFile},
                    {},
                    {},
                    {'label': 'BACK', 'id': 'bckBtn', 'funct': self.goBack}
                )
            ]

        super().__init__(app, prevView)
        self.numBtnX = self.cax
        self.numBtnY = self.cay

        self.folderList = []
        
        if os.path.exists(d.USB_DATA_PATH+d.TESTS_DIR):
            self.testsPath = d.USB_DATA_PATH+d.TESTS_DIR
        else:
            self.testsPath = d.RASPI_DATA_PATH+d.TESTS_DIR
        l = self.getAllFolders()      
        self.folderList.append(nl.NoteList(self.app, self.disp,{'x':self.cax-23*d.px,'y':self.cay, 'xdim':28*d.px, 'ydim': 50*d.py}, l,'Test folders', True))
        
        
        l = [fullName[0:-4] for fullName in self.getAllFiles(self.folderList[0].getItem())]     
        self.folderList.append(nl.NoteList(self.app, self.disp,{'x':self.cax+15*d.px,'y':self.cay, 'xdim':40*d.px, 'ydim': 50*d.py}, l,self.folderList[0].getItem()+' Test files', False))
        
#         self.focus = 0
#         self.folderList[self.focus].setFocus(True)
    def replaceList(self, l, folder):
        self.folderList[1] = (nl.NoteList(self.app, self.disp,{'x':self.cax+15*d.px,'y':self.cay, 'xdim':40*d.px, 'ydim': 50*d.py}, l, folder + ' Test files', False))
        
    def getDirectSubDirs(self,dirPath):
        return [name for name in os.listdir(dirPath) if os.path.isdir(os.path.join(dirPath, name))]

    def getMostRecent(self):
        pass
    def getAllFolders(self):
        return self.getDirectSubDirs(self.testsPath)    
    def getAllFiles(self, testFolderName):
        path = self.testsPath +'/'+testFolderName
        testFiles = [tf for tf in os.listdir(path) if os.path.isfile(os.path.join(path, tf))]
        return testFiles

    def selectFolder(self):
        testFolderName = self.folderList[self.focusNum].getItem()        
        path = self.testsPath +'/'+testFolderName
        testFiles = [tf for tf in os.listdir(path) if os.path.isfile(os.path.join(path, tf))]
    def selectFile(self):
        testFolderName = self.folderList[0].getItem()
        print(testFolderName)

        testFile = self.folderList[1].getItem()
               
        path = self.testsPath +'/'+testFolderName+'/'+testFile
        from views import testFileView as tfv
        self.app.setView(tfv.TestFileView(self.app, path, self))
        

    def upArrowPress(self):
        self.folderList[self.focusNum].upArrowPress()
        if self.focusNum ==0:
            self.replaceList(self.getAllFiles(self.folderList[0].getItem()), self.folderList[0].getItem())
    def downArrowPress(self):
        self.folderList[self.focusNum].downArrowPress()
        if self.focusNum ==0:
            self.replaceList(self.getAllFiles(self.folderList[0].getItem()), self.folderList[0].getItem())
    def leftArrowPress(self):

        self.folderList[self.focusNum].setFocus(False)
        self.focusNum = not self.focusNum
        self.folderList[self.focusNum].setFocus(True)
        self.initButArea()

    def rightArrowPress(self):

        self.folderList[self.focusNum].setFocus(False)
        self.focusNum = not self.focusNum
        self.folderList[self.focusNum].setFocus(True)
        self.initButArea()

    def displayView(self):
        for fl in self.folderList:
            fl.display()