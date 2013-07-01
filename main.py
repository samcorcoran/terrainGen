import sys
import math
import random

import pyglet
from pyglet.gl import *

import terrain
import draw

#print("Terrain!")

### Generation Parameters ###
windowDim = 800
n = 6

minHeight = 0
maxHeight = 1

roughness = 5

subdivisions = 4
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
print("gridDim: " + str(gridDim))

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
aMapWindow = draw.MapWindow(landscape, windowDim, blockDim, flatSea)
aMapWindow.createTiles()

print("Running app")
pyglet.app.run()
print("Ran app")
