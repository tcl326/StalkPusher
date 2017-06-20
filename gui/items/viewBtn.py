from main import defs as d
"""
ViewBtn: a basic UI item displayed as a rectangle with text
contains a label, a value, a function
has two states: focus / no focus 
"""
class ViewBtn:
    def __init__(self,
                 app,
                 pos,
                 dim,
                 label,
                 value
                 funct = None,
                 focus = False,
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
        
        self.rl = rl.RectLabel(self.app,
                               (self.x, self.y),
                               (self.xdim, self.ydim),
                               self.makeRlText(),
                               self.app.stnBtnFont,
                               self.app.font_col,
                               self.bcgCol
                               )
        
    def setValue(self, value):
        self.value = value
        self.rl.setText(self.makeLabel())
            
    def setFocus(self, focus):
        self.focus = focus
        self.rl.setBcgCol(d.textView_highlight_col if self.focus else self.app.textView_col)
        
    def makeRlText(self):
        return self.label+ ': ' + str(self.value) + ('mm' if self.label == 'Height' else '')
    
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
