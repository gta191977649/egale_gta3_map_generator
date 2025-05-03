# Class model for definations (Def)

class Defination:
    def __init__(self,zone,id,dff,col,txd,flag,lodDistance=299,timeIn=None,timeOut=None):
        self.zone = zone
        self.id = id
        self.dff = dff
        self.col = col
        self.txd = txd
        self.flag = flag
        self.lodDistance = lodDistance
        self.timeIn = timeIn
        self.timeOut = timeOut

    def __str__(self):
        return ' <definition id="{}" zone="{}" col="{}" txd="{}" flags="{}" lodDistance="{}"></definition>'.format(self.id, self.zone, self.col, self.txd, self.flag, self.lodDistance)
