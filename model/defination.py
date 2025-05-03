# Class model for definations (Def)

class Defination:
    def __init__(self, id,dff,col,txd,flag,lodDistance=299,timeIn=None,timeOut=None):
        self.id = id
        self.dff = dff
        self.col = col
        self.txd = txd
        self.flag = flag
        self.lodDistance = lodDistance
        self.timeIn = timeIn
        self.timeOut = timeOut

