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
    def __init__(self, app, pos, dim, text, font, fontCol = 0, bcgCol = d.bcg_col_d, txtMode = 'spt'):
        self.app = app
        self.disp = self.app.disp
        self.x = pos[0]
        self.y = pos[1]
        self.xdim = dim[0]
        self.ydim = dim[1]

        self.text = text
        
        self.font = font
        
        self.txtMode = txtMode
                
        if not fontCol:
            self.setFontCol(self.app.font_col)
        else:
            self.setFontCol(fontCol)  
                      
        self.bcgSurface = pg.Surface((self.xdim, self.ydim), pg.SRCALPHA)  # per-pixel alpha
        
        self.setBcgCol(bcgCol)
        
        self.setHasBorder(False)
        
    def setFontCol(self, fontCol):
        self.fontCol = fontCol

    def setBcgCol(self, bcgCol):
        self.bcgCol = bcgCol
                
    def setText(self, text):
        self.text = text
           
    def setHasBorder(self, hasBorder):
        self.hasBorder = hasBorder

    def display(self):
        self.show(self.x, self.y)
        
    def displayWithY(self, y):
        self.show(self.x, y)
    
    def show(self, x, y):
        self.s.fill(self.bcgCol)
        self.disp.blit(self.s, (x - self.xdim / 2, y - self.ydim / 2, self.xdim, self.ydim))
                
        if self.hasBorder:
            pg.draw.rect(self.disp, [0, 0, 255], (x - self.xdim/2,y - self.ydim / 2,self.xdim,self.ydim), 5)
            
        if self.txtMode == 'spu':
            txt.spu(self.disp,
                    self.text,
                    (self.x, self.y),
                    self.font,
                    self.fontCol)
        elif self.txtMode == 'spt':
            txt.spt(self.disp,
                    self.text,
                    (self.x, self.y),
                    self.xdim,
                    self.font,
                    self.fontCol)
        
        elif self.txtMode == 'mpue':
            txt.mpue(self.disp,
                    self.text,
                    (self.x, self.y),
                    self.ydim,
                    self.font,
                    self.fontCol)
            
        