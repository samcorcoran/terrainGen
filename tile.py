import math
import random

class Tile():
        def __init__(self, xLoc, yLoc, tileHeight, color):
        	self.xLoc = xLoc
        	self.yLoc = yLoc
        	self.height = tileHeight
        	self.color = color
        	#self.color = (random.random(), random.random(), random.random())

        def printTile(self):
        	print("Tile at (" + str(self.xLoc) + ", " + str(self.yLoc) + "), with height: "  + str(self.height) + " and color: " + str(self.color))