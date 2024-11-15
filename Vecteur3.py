class Vecteur3:
    def __init__(self,x:int,y:int,z:int):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self,vec3):
        return Vecteur3(self.x+vec3.x, self.y+vec3.y,self.z+vec3.z)
