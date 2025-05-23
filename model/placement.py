from quaternion import *

class Placement:
    def __init__(self,id,x,y,z,rx,ry,rz,rw):
        self.id = id
        self.x = x
        self.y = y
        self.z = z
        # Convert From Quanterion
        self.rx, self.ry, self.rz = from_quaternion(float(rx), float(ry), float(rz), float(rw))

# Building Object Type
class Building(Placement):
    def __init__(self, id, x=0, y=0, z=0, rx=0, ry=0, rz=0,rw=0, lodParent="self"):
        super().__init__(id, x, y, z, rx, ry, rz,rw)
        self.lodParent = lodParent

    def __str__(self):
        return '<building id="{}" posX="{}" posY="{}" posZ="{}" rotX="{}" rotY="{}" rotZ="{}" lodParent="{}"></building>'.format(self.id, self.x, self.y, self.z, self.rx, self.ry, self.rz, self.lodParent)

class Object(Placement):
    def __init__(self, id, x=0, y=0, z=0, rx=0, ry=0, rz=0,rw=0):
        super().__init__(id, x, y, z, rx, ry, rz,rw)

    def __str__(self):
        return '<object id="{}" posX="{}" posY="{}" posZ="{}" rotX="{}" rotY="{}" rotZ="{}"></object>'.format(self.id, self.x, self.y, self.z, self.rx, self.ry, self.rz)


