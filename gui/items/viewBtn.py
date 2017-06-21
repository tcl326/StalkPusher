"""
ViewBtn: a basic UI item displayed as a rectangle with text
contains a label, a value, a function
has two states: focus / no focus 
"""
from main import defs as d
from items import rectLabel as rl
class ViewBtn:
    def __init__(self,
                 app,
                 pos,
                 dim,
                 label,
                 value = '',
                 funct = None,
                 focus = False,
                 formating = lambda lab, val :lab
                ):
        self.app = app
        self.disp = self.app.disp
        
        #geo data
        self.x = pos[0]
        self.y = pos[1]
        self.xdim = dim[0]
        self.ydim = dim[1]
        
        #meta data
        self.label = label
        self.value = value
        self.funct = funct
        
        self.focus = focus
        
        self.formating = formating
        
        self.rl = rl.RectLabel(app=self.app,
                               pos=(self.x, self.y),
                               dim=(self.xdim, self.ydim),
                               text=self.formating(self.label, self.value),
                               font=self.app.stnBtnFont,
                               bcgCol=d.textView_highlight_col if self.focus else self.app.textView_col,
                               )
        
    def setValue(self, value):
        self.value = value
        self.rl.setText(self.formating(self.label, self.value))
            
    def setFocus(self, focus):
        self.focus = focus
        self.rl.setBcgCol(d.textView_highlight_col if self.focus else self.app.textView_col)
        
    def makeRlText(self):
        return self.label+ ': ' + str(self.value)
    
    def display(self):
        self.rl.display()

    def leftArrowPress(self):
        pass
    def rightArrowPress(self):
        pass
    def upArrowPress(self):
        pass
    def downArrowPress(self):
        pass
