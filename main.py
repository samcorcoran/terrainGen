import sys
import Tkinter as tk
import math
import random

import terrain
import draw

#print("Terrain!")

### Generation Parameters ###
windowDim = 800
n = 10

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

flatSea = True
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
landscape = terrain.Terrain(gridDim, gridDim, minHeight, maxHeight)

# Generate terrain
if useDiamondSquare:
        print("Generating 'Diamond Square' terrain with " + str(subdivisions) + " subdivisions.")
        landscape.seededDiamondSquare(0, 0, gridDim-1, gridDim-1, roughness, subdivisions, toroidal, fillSubGrids)
elif useMidpointDisplacement:
        print("Generating 'Midpoint Displacement' terrain with " + str(subdivisions) + " subdivisions.")
        landscape.seededMidpointDisplacement(0, 0, gridDim-1, gridDim-1, roughness, subdivisions, toroidal, fillSubGrids)
else:
        print("Generating random height field.")
        #landscape.randomiseCorners()
        landscape.randomiseHeights()

# Smooth terrain
if smoothTerrain:
        smoothness = int(math.ceil(gridDim/256.0))
        landscape.smoothHeights(smoothness, smoothingIterations)

#landscape.printGridTransposed()

# Draw
t = tk.Tk()
aMap = draw.Map(t, landscape, windowDim, blockDim, flatSea)
t.bind_all('<Key>', aMap.keyPressed)
aMap.createRects()
while True:
        aMap.applyKeyPressOffsets()
        if aMap.mapChanged:
                aMap.updateRects()
                aMap.mapChanged = False
        aMap.updateCanvas()
t.mainloop()
