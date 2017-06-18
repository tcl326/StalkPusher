'''
rectLabel.py created by Witold on 2/2/2017 under the cropDevice project
disp:display object
geoData {x,y,xdim,ydim}
txtData {label, txtDim, color}
'''
import pygame as pg
import defs as d
from utils import text as txt

class RectLabel:
    def __init__(self, app, geoData, txtData, fontCol = 0, wrap = 'single-inline'):
        self.app = app
        self.disp = self.app.disp
        self.x = geoData['x']
        self.y = geoData['y']
        self.xdim = geoData['xdim']
        self.label = txtData['txt']
        self.displayStr = self.label
        self.ydim = geoData['ydim']
        
        self.txtDim = int(txtData['txtDim'])
        
        self.wrap = wrap
        
        self.setFont(self.txtDim)
        
        if not fontCol:
            self.setFontCol(self.app.font_col)
        else:
            self.setFontCol(fontCol)  
                      
#         self.setTxt(self.label)
        self.s = pg.Surface((self.xdim, self.ydim), pg.SRCALPHA)  # per-pixel alpha
        self.setBcgCol(txtData['color'])
#         self.s.fill(self.bcgCol)
        self.setHasBorder(False)
        
        self.setTxt(self.displayStr)

        self.hasBorder = False
    def setBcgCol(self, bcgCol):
        self.bcgCol = bcgCol
        self.s.fill(self.bcgCol)
        
    def setHasBorder(self, hasBorder):
        self.hasBorder = hasBorder
        
    def setFontCol(self, fontCol):
        self.fontCol = fontCol
#         self.setTxt(self.label)

    def setFont(self, dim):
#         self.font = pg.font.SysFont('Arial', int(dim), bold = True)
        
        if self.wrap == 'single-inline':
            self.displayStr , self.txtDim = txt.findInclString(self.label, 'Arial', self.xdim, self.ydim)            
            self.font = pg.font.SysFont('Arial', self.txtDim, bold = True)
        else:
            self.font = pg.font.SysFont('Arial', txt.findFontSize(self.displayString, 'Arial', self.xdim, self.ydim, 4*d.px), bold = True, wrap = self.wrap)#self.txtDim

    def setTxt(self, label):
        self.txt = self.font.render(str(label), True, self.fontCol)
        self.display()
    
    def display(self):
        self.show(self.x, self.y)
    
    def displayWithY(self, y):
        self.show(self.x, y)
    
    def show(self, x, y):
        self.disp.blit(self.s, (x - self.xdim / 2, y - self.ydim / 2, self.xdim, self.ydim))
        self.disp.blit(self.txt, (self.txt.get_rect(center=(x, y))))
        if self.hasBorder:
            pg.draw.rect(self.disp, [0, 0, 255], (x - self.xdim/2,y - self.ydim / 2,self.xdim,self.ydim), 5)
        self.app.updateScreen()
