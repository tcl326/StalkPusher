import pygame as pg
import defs as d
from items import rectLabel as rl

class Message:
    def __init__(self, app, view, disp, ttlTxt, msgTxt,
                  geoData = {'x':62.5*d.px, 'y': 50*d.py, 'xdim': 70*d.px, 'ydim': 50*d.py},
                  btnDefs = None):
        
        self.app = app
        self.disp = disp
        self.view = view
        
        self.ttlTxt = ttlTxt
        self.msgTxt = msgTxt
        
        self.btnDefs = btnDefs
        
        self.x = geoData['x']
        self.y = geoData['y']
        self.xdim = geoData['xdim']
        self.ydim = geoData['ydim']
        
        
        self.bcg = pg.Surface((self.xdim, self.ydim), pg.SRCALPHA)  # per-pixel alpha

        self.bcg.fill(self.app.textView_col)
        self.ttl = rl.RectLabel(self.app,
                                {'x':self.x, 'y': self.y - self.ydim/2 + 5*d.py, 'xdim': 70*d.px, 'ydim': 10*d.py},
                                {'txt':self.ttlTxt,'txtDim':4*d.px,'color':d.brightenColor(self.app.textView_col)})
        
        self.msg = rl.RectLabel(self.app,
                                {'x':self.x, 'y': self.y, 'xdim': 70*d.px, 'ydim': 10*d.py},
                                {'txt':self.msgTxt,'txtDim':2.5*d.px,'color':self.app.textView_col})
        self.initButArea()
    def initButArea(self):
        self.view.initButAreaByDefs(self.btnDefs)
          
    def display(self):
        #display message background rect
        self.disp.blit(self.bcg, (self.x - self.xdim / 2, self.y - self.ydim / 2, self.xdim, self.ydim))
        #display title
        self.ttl.display()
        #display message
        self.msg.display()
        