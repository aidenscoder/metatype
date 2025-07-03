from dataclasses import dataclass
@dataclass
class mutable:
    value:object
    mutable:bool = True

            
class point2D(tuple):
    def __new__(cls,x:int,y:int):
        return super().__new__(cls,[mutable(x),mutable(y)])
    
    @property
    def x(self):return self[0].value
        
    @x.setter
    def x(self,new_value):self[0].value = new_value
        
        

    @property
    def y(self):return self[1].value
        
    @y.setter
    def y(self,new_value):self[1].value = new_value
        