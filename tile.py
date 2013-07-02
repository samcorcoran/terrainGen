import math
import random

class Tile():
    def __init__(self, xLoc, yLoc, length, altitude):
        	self.xLoc = xLoc
        	self.yLoc = yLoc
        	self.length = length
        	self.altitude = altitude

        	# Initialize color with grayscale altitude values
        	self.color = (altitude, altitude, altitude)
        	#self.color = (random.random(), random.random(), random.random())

    def printTile(self):
        	print("Tile at (" + str(self.xLoc) + ", " + str(self.yLoc) + "), with length: "  + str(self.length) + " and color: " + str(self.color))

    def calculateTerrainColor(self, useColor, doInterp):
    	# If flag is false, color attribute will remain greyscale
    	if useColor:
    		self.color = self.getAltitudeColor(doInterp)

    def getAltitudeColor(self, doInterp):
        # Altitude proportions at which different terrain colors end
        
        # Color bands (terrain altitude cut offs, e.g. 0.65 seaLevel means that altitudes below 0.65 are sea)
        # Palette: Island Contouring
        self.seaLevel = 0.65
        self.sandLevel = 0.68
        self.grassLevel = 0.85
        self.hillLevel = 0.92
        self.mountainLevel = 0.98
        self.minHeightForShadows = self.seaLevel

        # Palette: In-land hills and mountains colouring
        #self.minHeightForShadows = 0.15
        #seaLevel = 0.15 * 255
        #sandLevel = 0.2 * 255
        #grassLevel = 0.55 * 255
        #hillLevel = 0.75 * 255
        #mountainLevel = 0.9 * 255

        seaLevelCol = self.seaLevel
        sandLevelCol = self.sandLevel
        grassLevelCol = self.grassLevel
        hillLevelCol = self.hillLevel
        mountainLevelCol = self.mountainLevel

        if self.altitude < seaLevelCol:
            seaMin = 0.2
            seaMax = 0.55
            t = 0.5
            if doInterp:
                t = self.altitude/seaLevelCol
            c = seaMin + t*(seaMax-seaMin)
            chosenColor = [0, 0, c]
        elif self.altitude < sandLevelCol:
            sandMin = 0.3
            sandMax = 0.5
            # Interpolation is reversed so low-sand is light green and high-grass is dark green
            t = 0.5
            if doInterp:
                t = 1-((self.altitude-seaLevelCol)/(sandLevelCol-seaLevelCol))
            c = sandMin + t*(sandMax-sandMin)
            chosenColor = [c, c, 0]
            #chosenColor = [255, 0, 0]
        elif self.altitude < grassLevelCol:
            grassMin = 0.12
            grassMax = 0.31
            t = 0.5
            if doInterp:
                # Interpolation is reversed so low-grass is light green and high-grass is dark green
                t = 1-((self.altitude-sandLevelCol)/(grassLevelCol-sandLevelCol))
            c = grassMin + t*(grassMax-grassMin)
            chosenColor = [0, c, 0]
        elif self.altitude < hillLevelCol:
            hillMin = 0.12
            hillMax = 0.22
            t = 0.5
            if doInterp:
                t = ((self.altitude-grassLevelCol)/(hillLevelCol-grassLevelCol))
            c = hillMin + t*(hillMax-hillMin)                        
            chosenColor = [c, c, 0]
        elif self.altitude < mountainLevelCol:
            mountainMin = 0.24
            mountainMax = 0.67
            t = 0.5
            if doInterp:
                t = ((self.altitude-hillLevelCol)/(mountainLevelCol-hillLevelCol))
            c = mountainMin + t*(mountainMax-mountainMin)                        
            chosenColor = [c, c, c]
        else:
            snowMin = 0.78
            snowMax = 1
            t = 0.5
            if doInterp:
                t = ((self.altitude-mountainLevelCol)/(1-mountainLevelCol))
            c = snowMin + t*(snowMax-snowMin)
            chosenColor = [c, c, c]

        # Ensure integer values for colors
        #chosenColor = [int(chosenColor[0])/255, int(chosenColor[1])/255, int(chosenColor[2])/255]
        #print("chosen color: " + str(chosenColor))

        # Apply shadowing
        #if self.useShadows:
        #    shadowing = min((1 - self.getLocShadowing(x, y)) * (1-self.shadowStrength), 1)
        #    chosenColor[0] = int(chosenColor[0] * shadowing)
        #    chosenColor[1] = int(chosenColor[1] * shadowing)
        #    chosenColor[2] = int(chosenColor[2] * shadowing)
        
        return chosenColor