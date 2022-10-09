from PIL import Image
import random
import numpy as np

cells = []

w, h = 10, 10
cells = [[[random.randint(0,255),random.randint(0,255),random.randint(0,255)] for x in range(w)] for y in range(h)] 

with open("mapa.txt", 'w') as file:
        for row in cells:
            s = " ".join(map(str, row))
            file.write(s+'\n')

cells = np.array(cells)

ones = [[[1] for x in range(100)] for y in range(100)] 

cells = np.kron(cells, ones)
   
cells = cells.tolist()   
 
pixels = []

for i in range(len(cells)):
    for j in range(len(cells)):
        pixels.append(tuple(cells[i][j]))

png = Image.new('RGB', [1000,1000])
png.putdata(pixels)
png.save("map.png")



