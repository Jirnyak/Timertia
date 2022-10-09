from PIL import Image
from PIL import ImageFilter
import numpy as np

cells = []

mu, sigma = 500, 125 # mean and standard deviation

capital = open('money_buffer.txt', encoding="utf-8").read()

capital = int(float(capital))

if capital > 1000000:
    capital = 1000000

w, h = 1000, 1000
cells = [[0 for x in range(w)] for y in range(h)] 

for i in range(int(capital)):
    x = int(np.random.normal(mu, sigma, 1))%1000
    y = int(np.random.normal(mu, sigma, 1))%1000
    if cells[x][y] == 0:
        cells[x][y] = (255, 200, 0)
    else:
        o = cells[x][y][1]
        o += 5
        if o > 255:
            o = 255
        cells[x][y] = (255, o, 0)
        
         
pixels = []

for i in range(len(cells)):
    for j in range(len(cells)):
        pixels.append(cells[i][j])

png = Image.new('RGB', [1000,1000])
png.putdata(pixels)
#png = png.filter(ImageFilter.BLUR)
png.save("gold.png")

