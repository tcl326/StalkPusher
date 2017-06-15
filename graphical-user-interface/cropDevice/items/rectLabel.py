'''
rectLabel.py created by Witold on 2/2/2017 under the cropDevice project
disp:display object
geoData {x,y,xdim,ydim}
txtData {label, txtDim, color}
'''
import pygame as pg
import defs as d

class RectLabel:
    def __init__(self, app, geoData, txtData, fontCol = 0):
        self.app = app
        self.disp = self.app.disp
        self.x = geoData['x']
        self.y = geoData['y']
        self.xdim = geoData['xdim']
        self.label = txtData['txt']
        self.ydim = geoData['ydim']
        self.txtDim = int(txtData['txtDim'])
        self.setFont(self.txtDim)
        if not fontCol:
            self.setFontCol(self.app.font_col)
        else:
            self.setFontCol(fontCol)            
        self.setTxt(self.label)
        self.s = pg.Surface((self.xdim, self.ydim), pg.SRCALPHA)  # per-pixel alpha
        self.setBcgCol(txtData['color'])
#         self.s.fill(self.bcgCol)
        self.setHasBorder(False)

        self.hasBorder = False
    def setBcgCol(self, bcgCol):
        self.bcgCol = bcgCol
        self.s.fill(self.bcgCol)
    def setHasBorder(self, hasBorder):
        self.hasBorder = hasBorder
    def setFontCol(self, fontCol):
        self.fontCol = fontCol
        self.setTxt(self.label)

    def setFont(self,dim):
        self.font = pg.font.SysFont('Arial', int(dim), bold = True)
#         self.setTxt(self.label)

    def setTxt(self, label):
        self.txt = self.font.render(str(label), True, self.fontCol)
    def display(self):
        self.show(self.x, self.y)
    def displayWithY(self, y):
        self.show(self.x, y)
    def show(self, x, y):
        self.disp.blit(self.s, (x - self.xdim / 2, y - self.ydim / 2, self.xdim, self.ydim))
        self.disp.blit(self.txt, (self.txt.get_rect(center=(x, y))))
        if self.hasBorder:
            pg.draw.rect(self.disp, [0, 0, 255], (x - self.xdim/2,y - self.ydim / 2,self.xdim,self.ydim), 5)