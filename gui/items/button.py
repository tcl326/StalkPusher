import pygame as pg
import defs as d
class Button:
    def __init__(self, app, bluePrint, geoData):
        # x, y, width, height, label, name, function
        self.app = app
        self.disp = self.app.disp
        self.x = geoData['x']
        self.y = geoData['y']
        self.xdim = geoData['xdim']
        self.ydim = geoData['ydim']
        self.id = bluePrint['id']
        self.funct = bluePrint['funct']
        self.setBcgCol()
        self.setFontCol()
        from utils import text as t
        self.font = pg.font.SysFont('Arial', t.findFontSize(bluePrint['label'], 'Arial',self.xdim, self.ydim, 4*d.px), bold = True)#int(3.2*d.px)
        self.txt = self.font.render(bluePrint['label'], True, self.fontCol)
    def setBcgCol(self):

#         if (self.id == 'bckBtn' or self.id == 'cancelBtn' or self.id == 'noBtn'):
#             self.bcgCol = d.textView_neg_col
#         elif (self.id == 'saveBtn' or self.id == 'yesBtn' or self.id == 'startBtn'):
#             self.bcgCol = d.textView_pos_col
#         else:
            self.bcgCol = self.app.textView_col
    def setFontCol(self):
        self.fontCol = self.app.font_col
    def display(self):
        pg.draw.rect(self.disp, self.bcgCol, (self.x-self.xdim/2, self.y-self.ydim/2, self.xdim, self.ydim))
        self.disp.blit(self.txt, (self.txt.get_rect(center=(self.x, self.y))))

    def removeUI(self):
        pass

    def action(self):
        if callable(self.funct):
            self.funct()
        elif type(self.funct == type(tuple)):
            for fun in self.funct:
                if callable(fun):
                    fun()
