'''
noteList.py created by Witold on 2/1/2017 under the cropDevice project
Item that displays and manages a list of notes.
startIndex denotes which item in the list should be displayed first
endIndex denotes which item in the list should be displayed last
only items between startIndex inclusive and endIndex inclusive are displayed
at the bginning, startIndex is 0; endIndex is either the number of items in list -1
or length of the array of y positions -1 (depending on the length of the list).
the start and end indices are updated when the following happens:
arrowUp AND startIndex!= 0 AND focusNum ==startIndex:
    startIndex -= 1, endIndex-=1, for i in range yNotesCents setYPos of notes between startIndex and endIndex to yNotesCents[i]
arrowDown AND endIndex!= len(list)-1 AND focusNum ==len(yNotesCents)-1:
    startIndex += 1, endIndex+=1, for i in range yNotesCents setYPos of notes between startIndex and endIndex to yNotesCents[i]
item from list removed (between startIndex and endIndex:
    remove corresponding item from notes list, if endIndex == len(list) --> endIndex -=1,
    for i in range yNotesCents setYPos of notes between startIndex and endIndex to yNotesCents[i]
    or that latter action can be started from the index of removal
item added to list (between startIndex and endIndex:
    if endIndex == len(list)-1 and startIndex == 0 --> endIndex++
    add corresponding item to notes list to the end

'''
import pygame as pg
import defs as d
from main import img
from items import rectLabel as rl
itemsAvImg = pg.image.load(d.APP_PATH + '/assets/img/itemsAv.png')
itemsAvImg = pg.transform.scale(itemsAvImg, (int(4*d.px), int(1*d.px)))


class NoteList():
    def __init__(self, app, disp, geoData, list = None, listName='', hasFocus=False, maxNotes = 50):
        self.app = app
        self.disp = disp
        self.x = geoData['x']
        self.y = geoData['y']
        self.xdim = geoData['xdim']
        self.ydim = geoData['ydim']
        self.listName = listName
        self.maxNotes = maxNotes
        if list is not None:
            self.list = list
        else:
            self.list = self.app.getSetting(self.listName)
        self.focusNum = 0
        self.determineLayout()
        # self.setFocus(hasFocus)
        self.hasFocus = hasFocus
        self.addNotes()

        self.addTtlRect()
#     @classmethod
#      def fromListName(cls, app, disp, geoData, listName, hasFocus):
#          list = app.getSetting(self.listName)
#          return cls(app, disp, geoData, list, hasFocus)
    
    def addTtlRect(self):
        self.ttlRect = rl.RectLabel(
            self.app,
            {'x':self.x,
             'y':self.y-self.ydim /2 - 8*d.py,
             'xdim': self.xdim,
             'ydim': self.noteHeight},
            {'txt':self.listName,
             'txtDim': 3*d.px,
             'color': d.transparent
             }, d.font_col_inv
            )
#         self.ttlRect.setFontCol(d.font_col_inv)
    def getItem(self):
        return self.list[0] if len(self.list) ==1 else self.list[self.focusNum]
    def saveList(self):
        d.saveSetting(self.listName, self.list)
    def isEmpty(self):
        return not self.list
    def isFull(self):
        return len(self.list) >= self.maxNotes
    def setFocus(self, focus):
        # if self.hasFocus != focus:
        self.hasFocus = focus
        if self.isEmpty():return
        if self.hasFocus:
#             self.setFocusNum(focusNum)
            self.notes[self.focusNum].setFocus(True)
        else:
            if not self.isEmpty():
                self.notes[self.focusNum].setFocus(False)
#     def hasFocus(self):
#         return self.hasFocus
    def determineLayout(self):
        self.noteHeight = 5*d.py
        self.interNoteSpace = 1*d.py
        yNoteCent =  self.y-self.ydim/2 + self.interNoteSpace + self.noteHeight/2
        self.yNoteCents = []

        while yNoteCent < self.y + self.ydim/2 - self.noteHeight/2:

            self.yNoteCents.append(yNoteCent)
            yNoteCent += (self.noteHeight + self.interNoteSpace)

        self.startIndex = 0
        self.endIndex = min(len(self.yNoteCents)-1, len(self.list)-1)
        self.itemsAvUplbl = rl.RectLabel(self.app,
                                         {'x': self.x, 'y': self.yNoteCents[0]- self.noteHeight - self.interNoteSpace, 'xdim': self.xdim,'ydim': self.noteHeight},
                                         {'txt': '...', 'txtDim': 4*d.px, 'color': self.app.textView_col})

        self.itemsAvDownlbl = rl.RectLabel(self.app,
                                         {'x': self.x, 'y': self.yNoteCents[-1]+ self.noteHeight+ self.interNoteSpace, 'xdim': self.xdim,'ydim': self.noteHeight},
                                         {'txt': '...', 'txtDim': 4*d.px, 'color': self.app.textView_col})

    def setFocusNum(self, focusNum):#focusNum operates on self.list (and hence self.notes)
#         if self.hasFocus:
        if self.isEmpty(): return
        self.notes[self.focusNum].setFocus(False)
        self.focusNum = focusNum
#         if self.hasFocus:
        self.notes[self.focusNum].setFocus(True)

    def addNotes(self):
        self.notes = []
        for i in range(len(self.list)):
            self.notes.append(self.Note(self.app,
                                        {'x': self.x,'y': self.y,'xdim': self.xdim,'ydim': self.noteHeight},
                                        {'txt':self.list[i], 'txtDim': 3*d.px},
                                        self.focusNum == i and self.hasFocus))
        self.itemsAvDownlbl.setTxt('+'+str(len(self.list)-self.endIndex-1)+'...')

    def printInfo(self):
        print('yNoteCents:',len(self.yNoteCents),'start:',self.startIndex, 'end:', self.endIndex, 'focusNum:', self.focusNum)
    def reSetItemsAv(self):
        self.itemsAvUplbl.setTxt('+'+str(self.startIndex)+'...')           
        self.itemsAvDownlbl.setTxt('+'+str(len(self.list)-self.endIndex-1)+'...')
        
    def prependNote(self, noteContent):
        self.list.insert(0, noteContent)
        self.notes.insert(0, self.Note(self.app,
                                        {'x': self.x,'y': self.y,'xdim': self.xdim,'ydim': self.noteHeight},
                                        {'txt':noteContent, 'txtDim': 3*d.px},
                                        False))
#         self.setFocusNum(0)
#         if self.endIndex - self.startIndex < len(self.yNoteCents)-1:
#             self.endIndex += 1
#         if self.focusNum == -1:
#             self.setFocusNum(0)
#         self.refocusOn(0)
        if self.startIndex>0:
            self.startIndex += 1
            self.endIndex +=1
 
#             if self.endIndex - self.startIndex < len(self.yNoteCents)-1:            
#                 self.endIndex -=1

        else:
            if self.endIndex - self.startIndex < len(self.yNoteCents)-1:            
                self.endIndex +=1
        if self.hasFocus:
            if self.endIndex == 0:
                self.setFocusNum(self.focusNum)
            elif self.focusNum == self.endIndex +1:
                self.setFocusNum(self.focusNum-1)
            else:
                self.setFocusNum(self.focusNum+1)
                
        self.reSetItemsAv()
    def refocusOn(self, num):#startIndex
        self.startIndex = num
        self.endIndex = min(len(self.list)-self.startIndex-1, len(self.list)-1)
        
        self.setFocusNum(self.startIndex)
        self.itemsAvUplbl.setTxt('+'+str(self.startIndex)+'...')           
        self.itemsAvDownlbl.setTxt('+'+str(len(self.list)-self.endIndex-1)+'...')

    def appendNote(self, noteContent):
        self.list.append(noteContent)
        self.notes.append(self.Note(self.app,
                                        {'x': self.x,'y': self.y,'xdim': self.xdim,'ydim': self.noteHeight},
                                        {'txt':noteContent, 'txtDim': 3*d.px},
                                        False))
        if self.endIndex - self.startIndex < len(self.yNoteCents)-1:
            self.endIndex += 1
        if self.focusNum == -1:
            self.setFocusNum(0)
        self.reSetItemsAv()
        

    def removeNote(self):
        if self.isEmpty(): return
        noteContent = self.list[self.focusNum]
        if len(self.notes) - self.startIndex <= len(self.yNoteCents):# self.endIndex - self.startIndex <= len(self.yNoteCents):
            self.endIndex -=1
            if self.startIndex > 0:
                self.startIndex -=1
        elif len(self.notes) - self.startIndex > len(self.yNoteCents):
            pass
        del self.list[self.focusNum]
        del self.notes[self.focusNum]
        # if self.isEmpty():
        #     self.focus
        if self.focusNum > 0:
            self.focusNum -= 1
        if not self.isEmpty():
            self.notes[self.focusNum].setFocus(True)
            
        self.reSetItemsAv()

        return noteContent
    def display(self):
        #display background rec
        #display each note
        self.ttlRect.display()
        for i in range(len(self.yNoteCents)):
            if i>=len(self.list):
                break
            self.notes[self.startIndex + i].display(self.yNoteCents[i])
        img.getLeftUp(itemsAvImg,self.x, self.y)
        if self.startIndex > 0:
            self.itemsAvUplbl.display()
            # self.disp.blit(itemsAvImg, img.getLeftUp(itemsAvImg, self.x, self.yNoteCents[0] - self.noteHeight))
        if self.endIndex != len(self.list) -1:
            self.itemsAvDownlbl.display()
            # self.disp.blit(itemsAvImg, img.getLeftUp(itemsAvImg, self.x, self.yNoteCents[-1] + self.noteHeight))

    def upArrowPress(self):
        if self.isEmpty(): return
        if self.focusNum == self.startIndex:
            if self.startIndex > 0:
                #move all downwards by decrementing startIndex and endIndex
                self.startIndex -= 1
                self.endIndex -= 1
                self.setFocusNum(self.focusNum -1)
        elif self.focusNum > self.startIndex:
            self.setFocusNum(self.focusNum - 1)
        
        
        self.reSetItemsAv()

    def downArrowPress(self):
        if self.isEmpty(): return

        if self.focusNum == self.endIndex:
            if self.endIndex < len(self.list)-1:
                #move all downwards by decrementing startIndex and endIndex
                self.startIndex += 1
                self.endIndex += 1
                self.setFocusNum(self.focusNum +1)
        elif self.focusNum < self.endIndex:
            self.setFocusNum(self.focusNum + 1)
        self.reSetItemsAv()

    def selectCurrent(self):
        if not self.isEmpty():
            self.notes[self.focusNum].selectToggle()
    def selectCurrentExclusive(self):
        if not self.isEmpty():
            for ind in range(len(self.notes)):
                if ind == self.focusNum:
                    self.notes[ind].select()
                else:
                    self.notes[ind].deselect()
                    
            
    def selectByItem(self, item):
        for ind in range(len(self.list)):
            if item == self.list[ind]:
                self.notes[ind].select()
                break
    def getSelected(self):
        selNotes = []
        for note in self.notes:
            if note.isSelection():
                selNotes.append(note.label)
        return selNotes
    
    def getSelectedExclusive(self):
        for note in self.notes:
            if note.isSelection():
                return note.label
    def isCurrentSelected(self):
        if not self.isEmpty():
            return self.notes[self.focusNum].isSelection()
        return False
    class Note:
        def __init__(self, app, geoData, txtData, focus):
            self.app = app
            self.disp = self.app.disp
            self.x = geoData['x']
            self.y = geoData['y']
            self.xdim = geoData['xdim']
            self.ydim = geoData['ydim']
            self.label = txtData['txt']
            self.txtDim = txtData['txtDim']
            txtData['color'] = self.app.font_col#d.light_blue if self.focus else d.light_gray
            self.rectLabel = rl.RectLabel(self.app, geoData, txtData)
            self.setFocus(focus)
            self.setIsSelected(False)
        def isSelection(self):
            return self.isSelected
        def setFocus(self, focus):
            self.focus = focus
            # self.rectLabel.setBcgCol(d.light_blue if self.focus else d.light_gray)
            self.rectLabel.setHasBorder(True if self.focus else False)
        def selectToggle(self):
            self.setIsSelected(not self.isSelected)
        def select(self):
            if not self.isSelection():
                self.setIsSelected(True)
        def deselect(self):
            if self.isSelection():
                self.setIsSelected(False)  
        def setIsSelected(self, isSelected):
            self.isSelected = isSelected
            self.rectLabel.setBcgCol(d.textView_highlight_col if self.isSelected else self.app.textView_col)
        def setYPos(self, y):
            self.y = y
        def display(self, y):
            self.rectLabel.displayWithY(y)