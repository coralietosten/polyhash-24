class Vecteur2:
    def __init__(self,x:int,y:int):
        self.x = int(x)
        self.y = int(y)

    def __str__(self):
        return f"[{self.x}, {self.y}]"
    
    def __repr__(self):
        return self.__str__()
    
    def __add__(self,vec2):
        return Vecteur2(self.x+vec2.x, self.y+vec2.y)
