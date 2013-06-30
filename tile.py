import math
import random

class Tile():
        def __init__(self, xLoc, yLoc, tileHeight):
        	self.xLoc = xLoc
        	self.yLoc = yLoc
        	self.height = tileHeight

        def printTile(self):
        	print("Tile at (" + str(self.xLoc) + ", " + str(self.yLoc) + "), with height = "  + str(self.height))