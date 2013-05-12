import sys
import tkinter
import math
import random

import terrain
import draw

#print("Terrain!")

### Generation Parameters ###
windowDim = 700
n = 3

minHeight = 0
maxHeight = 1

roughness = 5

subdivisions = 3
fillSubGrids = True
useDiamondSquare = False
useMidpointDisplacement = True

toroidal = True

smoothTerrain = True
smoothingIterations = 1
###

# Grid dimensions formula: (2^n)+1
gridDim = int(math.pow(2, n)) + 1

# Adjust window size to fit grid columns exactly
blockDim = 1
if gridDim > windowDim:
        blockDim = 1
        windowDim = gridDim
else:
        blockDim = int(windowDim / gridDim)
        windowDim = blockDim * gridDim
print("Window dimension set to: " + str(windowDim) + ", block width is: " + str(blockDim) + ", gridDim: " + str(gridDim))

# Create Terrain object
landscape = terrain.Terrain(gridDim, gridDim)

# Generate terrain
if useDiamondSquare:
        print("Generating 'Diamond Square' terrain with " + str(subdivisions) + " subdivisions.")
        landscape.seededDiamondSquare(0, 0, gridDim-1, gridDim-1, minHeight, maxHeight, roughness, subdivisions, toroidal, fillSubGrids)
elif useMidpointDisplacement:
        print("Generating 'Midpoint Displacement' terrain with " + str(subdivisions) + " subdivisions.")
        landscape.seededMidpointDisplacement(0, 0, gridDim-1, gridDim-1, minHeight, maxHeight, roughness, subdivisions, toroidal, fillSubGrids)
else:
        print("Generating random height field.")
        #landscape.randomiseCorners(minHeight, maxHeight)
        landscape.randomiseHeights(minHeight, maxHeight)

# Smooth terrain
if smoothTerrain:
        smoothness = int(math.ceil(gridDim/256.0))
        landscape.smoothHeights(smoothness, smoothingIterations)

#landscape.printGridTransposed()


# Draw
t = tkinter.Tk()
# Track key presses
right = False
left = False
up = False
down = False
def keyPressed(event):
        if event.keysym == 'left':
                left = True
        elif event.keysym == 'right':
                right = True
        elif event.keysym == 'up':
                up = True
        elif event.keysym == 'down':
                down = True
        else:
                return 0
t.bind_all('<Key>', keyPressed)

def resetKeys():
        up = True
        down = True
        left = True
        right = True

aMap = draw.Map(t, windowDim)

xOffset = 0
yOffset = 0
while True:
        if left: xOffset += -1
        elif right: offset += 1
        if up: yOffset += -1
        elif down: yOffset += 1
        xOffset = xOffset % windowDim
        yOffset = yOffset % windowDim

        if mapChanged:
                aMap.updateMap(t, landscape.grid, windowDim, blockDim, xOffset, yOffset)
                mapChanged = False
        aMap.updateCanvas()
t.mainloop()
