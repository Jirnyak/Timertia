from PIL import Image
import random
import math
from datetime import datetime
start=datetime.now()

class cell():

    def __init__(self,x,y,pos):
    
        self.x = x
        self.y = y
        
        self.pos = pos
    
        self.alive = 0  
        self.aliveB = 0

def sosedy(lis, pos):
    sos = []
    size = int(math.sqrt(len(lis)))
    if pos%size != 0 and pos > size and pos < len(lis)-1 - size:  
        sos.append(lis[pos-size-1])
        sos.append(lis[pos-size])
        sos.append(lis[pos-size+1])
        sos.append(lis[pos-1])
        sos.append(lis[pos+1])
        sos.append(lis[pos+size-1])
        sos.append(lis[pos+size])
        sos.append(lis[pos+size+1])
    return sos
black = 0 
while black < 1000:

    cells = []
    a = 0
    pixels = []
    black = 0

    for i in range(100):
        for j in range(100):
            cells.append(cell(j,i,i*100+j))
  
    for i in range(1000):  
        cells[random.randint(0,len(cells)-1)].alive = 1

    
    while a < 500:
        a+=1
        for obj in cells:
            check = sosedy(cells, obj.pos)
            score = 0 
            for k in check:
                score += k.alive 
            if score == 3 and obj.alive == 0:
                obj.aliveB = 1
            if score < 2 or score > 5:
                obj.aliveB = 0
                
        for obj in cells: 
            obj.alive = obj.aliveB
        
    for obj in cells:
            if obj.alive == 1:
                pixels.append((0,0,0))
                black+=1
            else:
                pixels.append((255,255,255))
 
    del cells[:]

            
                
png = Image.new('RGB', [100,100])
png.putdata(pixels)
png.save("maze10.png")
#print(datetime.now()-start)
      
        
      
        

        
       
    


        
        
    
            
        
        
    
    

