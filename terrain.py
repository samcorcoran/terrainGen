import Tkinter
import math
import random

#print("Terrain!")


class Terrain():
        def __init__(self, xDim, yDim):
                self.xDim = xDim
                self.yDim = yDim
                # Grid outer-list is of columns, inner list are of rows
                self.grid = [[1 for x in range(self.xDim)] for y in range(self.yDim)]

        def randomiseHeights(self, minHeight = 0, maxHeight = 1):
                self.grid = [[random.uniform(minHeight, maxHeight) for x in range(self.xDim)] for y in range(self.yDim)]

        def randomiseCorners(self, minHeight = 0, maxHeight = 1):
                
                self.grid[0][0] = random.uniform(minHeight, maxHeight)
                self.grid[len(self.grid)-1][0] = random.uniform(minHeight, maxHeight)
                self.grid[0][-1] = random.uniform(minHeight, maxHeight)
                self.grid[-1][-1] = random.uniform(minHeight, maxHeight)

        def smoothHeights(self, nhoodWidth = 3, iterations = 1):
                for i in range(iterations):
                        for x in range(len(self.grid)):
                                for y in range(len(self.grid[x])):
                                        self.grid[x][y] = self.neighbourhoodAverage(x, y, nhoodWidth)

        def getCoordHeight(self, x, y):
                # Ensure coordinate is inbounds
                if coordInBounds(x, y):
                                return self.grid[x][y]
                return False

        def coordInValidCol(self, x, y):
                if x < len(self.grid[0]) and x >= 0:
                        return True
                return False

        def coordInValidRow(self, x, y):
                if y < len(self.grid) and y >= 0:
                        return True
                return False
        
        def coordInBounds(self, x, y):
                return self.coordInValidRow(x, y) and self.coordInValidCol(x, y)
        
        def neighbourhoodAverage(self, x, y, nhoodWidth = 1):
                nhoodWidth = (nhoodWidth * 2) + 1
                total = 0
                counter = 0
                # If given coordinate is in bounds, check neighbour validity
                if self.coordInBounds(x, y):
                        left = self.coordInValidCol(x-1, y)
                        right = self.coordInValidCol(x+1, y)
                        above = self.coordInValidRow(x, y-1)
                        below = self.coordInValidRow(x, y+1)
                        for xOffset in range(nhoodWidth):
                                nX = x+(xOffset-1)
                                # Skip iteration along column if all coords will be invalid
                                if self.coordInValidCol(nX, y):
                                        for yOffset in range(nhoodWidth):
                                                nY = y+(yOffset-1)
                                                if self.coordInValidRow(nX, nY):
                                                        total += self.grid[nX][nY]
                                                        counter += 1
                                                        
                return 0 if counter == 0 else total/counter

        def printGrid(self):
                print("")
                if len(self.grid[0]) > 0:
                        # Repeat for each row
                        for rowNum in range(len(self.grid[0])):
                                # Form row-list from column elements
                                row = []
                                for column in self.grid:
                                        row.append(column[rowNum])
                                print(row)
                print("")
                
        def diamondSquare(self, x0 = 0, y0 = 0, x1 = 1, y1 = 1, roughness = 5): 
                # Continue if enclosed grid is not 2x2
                if x1 - x0 > 1:                 
                        # Diamond Step
                        midX = x0 + int(math.ceil((x1-x0)/2))
                        midY = y0 + int(math.ceil((y1-y0)/2))
                        
                        #print("midX: " + str(midX))
                        #print("midY: " + str(midY))
                        
                        # Collect corner heights
                        a = self.grid[x0][y0]
                        b = self.grid[x1][y0]
                        c = self.grid[x0][y1]
                        d = self.grid[x1][y1]
                        # Calculate midpoint height
                        cornerAvg = (a + b + c + d) / 4
                        maxDisplacement = int(math.pow(2, roughness) / 255)
                        maxDisplacement = 0.08
                        e = min(max(cornerAvg + random.uniform(-maxDisplacement, maxDisplacement), 0), 1)
                        self.grid[midX][midY] = e
                        
                        # Square step
                        # Left
                        self.grid[x0][midY] = min(max(((a + c + e) / 3) + random.uniform(-maxDisplacement, maxDisplacement), 0), 1)
                        # Above
                        self.grid[midX][y0] = min(max(((a + b + e) / 3) + random.uniform(-maxDisplacement, maxDisplacement), 0), 1)
                        # Right
                        self.grid[x1][midY] = min(max(((b + d + e) / 3) + random.uniform(-maxDisplacement, maxDisplacement), 0), 1)
                        # Below
                        self.grid[midX][y1] = min(max(((c + d + e) / 3) + random.uniform(-maxDisplacement, maxDisplacement), 0), 1)

                        # Begin recursion..
                        # Upper left
                        self.diamondSquare(x0, y0, midX, midY)
                        # Upper Right
                        self.diamondSquare(midX, y0, x1, midY)
                        # Lower Left
                        self.diamondSquare(x0, midY, midX, y1)
                        # Lower Right
                        self.diamondSquare(midX, midY, x1, y1)

        def midpointDisplacement(self, x0, y0, x1, y1, roughness, toroidal = False):
                #print("Starting with coords:" + str([x0, y0, x1, y1]))
                maxIndex = len(self.grid)-1
                if x0 == 0 and x1 == maxIndex:
                        if toroidal:
                                # Full grid, so make corners toroidal
                                # NE Corner
                                self.grid[maxIndex][0] = self.grid[0][0]
                                # SE Corner
                                self.grid[maxIndex][maxIndex] = self.grid[0][maxIndex]
                if x1 - x0 > 1:
                        # Find edge midpoint heights by averaging pairs of corners
                        halfwayX = int((x0 + x1) / 2)
                        halfwayY = int((y0 + y1) / 2)
                        #print(" Halfway: " + str(halfwayX) + " " + str(halfwayY))
                        # West
                        a = (self.grid[x0][y0] + self.grid[x0][y1]) / 2
                        self.grid[x0][halfwayY] = a
                        # North
                        b = (self.grid[x0][y0] + self.grid[x1][y0]) / 2
                        self.grid[halfwayX][y0] = b
                        # East
                        c = (self.grid[x1][y0] + self.grid[x1][y1]) / 2
                        self.grid[x1][halfwayY] = c
                        # South
                        d = (self.grid[x0][y1] + self.grid[x1][y1]) / 2
                        self.grid[halfwayX][y1] = d
                        # Calculate centre-point height
                        maxDisplacement = math.pow(2, roughness) / 255
                        #maxDisplacement = 0.1
                        e = min(max(((a + b + c + d) / 4) + random.uniform(-maxDisplacement, maxDisplacement), 0), 1)
                        self.grid[halfwayX][halfwayY] = e                     
                        # Perform recursion
                        # Upper-left
                        self.midpointDisplacement(x0, y0, halfwayX, halfwayY, roughness, toroidal) 
                        # Upper-right
                        self.midpointDisplacement(halfwayX, y0, x1, halfwayY, roughness, toroidal)                              
                        # Lower-left
                        self.midpointDisplacement(x0, halfwayY, halfwayX, y1, roughness, toroidal)                              
                        # Lower-right
                        self.midpointDisplacement(halfwayX, halfwayY, x1, y1, roughness, toroidal)

        def seededMidpointDisplacement(self, x0, y0, x1, y1, roughness, subdivisions, toroidal = False):
                subdivisions = int(math.pow(2, subdivisions))
                if x1 - x0 > 1:
                        stepSize = int((x1 - x0) / subdivisions)
                        if stepSize > 0:
                                print("step: " + str(stepSize))
                                print("grid Dim: " + str(gridDim))
                                # Seed values
                                for xSteps in range(subdivisions+1):
                                        for ySteps in range(subdivisions+1):
                                                self.grid[xSteps*stepSize][ySteps*stepSize] = min(max(random.uniform(0, 1), 0), 1)
                                if toroidal:
                                        # Average corner seeds
                                        cornerAvg = (self.grid[0][0] + self.grid[-1][0] + self.grid[0][-1] + self.grid[-1][-1]) / 4
                                        self.grid[0][0] = cornerAvg
                                        self.grid[0][-1] = cornerAvg
                                        self.grid[-1][0] = cornerAvg
                                        self.grid[-1][-1] = cornerAvg
                                        # Duplicate north edge as south edge
                                        for x in range(len(self.grid)):
                                                self.grid[x][-1] = self.grid[x][0]
                                        # Duplicate west edge as east edge
                                        for y in range(len(self.grid)):
                                                self.grid[-1][y] = self.grid[0][y]
                                # Perform midpoint displacement on subgrids
                                for xSteps in range(subdivisions):
                                        for ySteps in range(subdivisions):
                                                startX = xSteps*stepSize
                                                startY = ySteps*stepSize
                                                self.midpointDisplacement(startX, startY, startX+stepSize, startY+stepSize, roughness, toroidal)
                        else:
                                print("Seeding of midpoint displacement failed: stepsize too small")
                                        
        def printGridTransposed(self):
                print("")
                for column in self.grid:
                        print(column)
                print("")                       

# gridDim = (2^n)+1
n = 8
gridDim = int(math.pow(2, n)) + 1
minHeight = 0
maxHeight = 1
terrain = Terrain(gridDim, gridDim)
#terrain.printGrid()
#terrain.randomiseHeights(minHeight, maxHeight)
#terrain.printGrid()
#terrain.printGridTransposed()
#terrain.printGrid()
terrain.randomiseCorners(minHeight, maxHeight)
roughness = 5
# Generate terrain
#terrain.diamondSquare(0, 0, gridDim-1, gridDim-1, roughness)
terrain.seededMidpointDisplacement(0, 0, gridDim-1, gridDim-1, roughness, 3, True)

# Smooth terrain
smoothness = int(math.ceil(gridDim/256))
smoothingIterations = 4
terrain.smoothHeights(smoothness, smoothingIterations)


# Test value, to visually determine where coordinates lay
#terrain.grid[0][gridDim-1] = 0

# Graphics
windowDim = 700
if gridDim > windowDim:
        blockDim = 1
        windowDim = gridDim
else:
        blockDim = int(windowDim / gridDim)
        windowDim = blockDim * gridDim
print("Window dimension set to: " + str(windowDim) + ", block width is: " + str(blockDim) + ", gridDim: " + str(gridDim))
imageDim = windowDim

class App:
        def __init__(self, t, terrainGrid):
                self.i = Tkinter.PhotoImage(width=imageDim,height=imageDim)

                useColors = True
                colors = []
                # Iterate over columns
                for x in range(len(terrainGrid)):
                        # Iterate over rows
                        for y in range(len(terrainGrid[0])):
                                height = terrainGrid[x][y]
                                if useColors:
                                        color = self.getTerrainColor(height)
                                else:
                                        intensity = int(((height-minHeight)/maxHeight) * 255)
                                        color = [intensity for i in range(3)]
                                colors.append(color)

                c = Tkinter.Canvas(t, width=imageDim, height=imageDim); c.pack()

                macroRow = 0; macroCol = 0              
                if gridDim == windowDim:
                        # Add pixels to canvas
                        for color in colors:
                                for x in range(blockDim):
                                        for y in range(blockDim):
                                                row = (macroRow * blockDim) + y
                                                col = (macroCol * blockDim) + x
                                                rowString = str(macroRow) + "*" + str(blockDim) + "+" + str(y) + "=" + str(row)
                                                colString = str(macroCol) + "*" + str(blockDim) + "+" + str(x) + "=" + str(col)
                                                rowString = str(row)
                                                colString = str(col)
                                                #print("   Handling " + rowString+", " + colString )
                                                self.i.put('#%02x%02x%02x' % tuple(color),(row,col))
                                macroCol += 1
                                # After last column of colours in row, move to start of next row
                                if macroCol == gridDim:
                                        macroRow +=1; macroCol = 0
                else:
                        # Draw colors as rects
                        for color in colors:
                                # Get rect coords
                                x0 = macroCol * blockDim
                                y0 = macroRow * blockDim
                                x1 = x0 + blockDim
                                y1 = y0 + blockDim
                                # Draw Rect
                                strCol = '#%02x%02x%02x' % tuple(color)
                                # NOTE: Canvas coordinates start from bottom-left, so rectangles transpose terrain
                                c.create_rectangle(x0, y0, x1, y1, outline = strCol, fill = strCol)

                                #c.create_rectangle(x0, y0, x1, y1,  fill = strCol)

                                # Increment counters
                                macroCol += 1
                                # After last column of colours in row, move to start of next row
                                if macroCol == gridDim:
                                        macroRow +=1; macroCol = 0
                c.create_image(0, 0, image = self.i, anchor=Tkinter.NW)

        def getTerrainColor(self, height):
                # Height proportions at which different terrain colors end
                height *= 255
                
                # In-land hills and mountains colouring
                #seaLevel = 0.15 * 255
                #sandLevel = 0.2 * 255
                #grassLevel = 0.55 * 255
                #hillLevel = 0.75 * 255
                #mountainLevel = 0.9 * 255
                
                # Island colouring
                seaLevel = 0.65 * 255
                sandLevel = 0.68 * 255
                grassLevel = 0.85 * 255
                hillLevel = 0.92 * 255
                mountainLevel = 0.98 * 255
                
                if height < seaLevel:
                        seaMin = 50
                        seaMax = 140
                        t = height/seaLevel
                        c = seaMin + t*(seaMax-seaMin)
                        chosenColor = [0, 0, c]
                elif height < sandLevel:
                        sandMin = 75
                        sandMax = 125
                        # Interpolation is reversed so low-sand is light green and high-grass is dark green
                        t = 1-((height-seaLevel)/(sandLevel-seaLevel))
                        c = sandMin + t*(sandMax-sandMin)
                        chosenColor = [c, c, 0]
                        #chosenColor = [255, 0, 0]
                elif height < grassLevel:
                        grassMin = 30
                        grassMax = 80
                        # Interpolation is reversed so low-grass is light green and high-grass is dark green
                        t = 1-((height-sandLevel)/(grassLevel-sandLevel))
                        c = grassMin + t*(grassMax-grassMin)
                        chosenColor = [0, c, 0]
                elif height < hillLevel:
                        hillMin = 30
                        hillMax = 55
                        t = ((height-grassLevel)/(hillLevel-grassLevel))
                        c = hillMin + t*(hillMax-hillMin)                        
                        chosenColor = [c, c, 0]
                elif height < mountainLevel:
                        mountainMin = 60
                        mountainMax = 170
                        t = ((height-hillLevel)/(mountainLevel-hillLevel))
                        c = mountainMin + t*(mountainMax-mountainMin)                        
                        chosenColor = [c, c, c]
                else:
                        snowMin = 200
                        snowMax = 255
                        t = ((height-mountainLevel)/(1-mountainLevel))
                        c = snowMin + t*(snowMax-snowMin)
                        chosenColor = [c, c, c]
                # Scale color values for RGB
                #chosenColor = [min(max(int(chosenColor[0] * 255),0), 255), min(max(int(chosenColor[1] * 255),0), 255), min(max(int(chosenColor[2] * 255),0), 255)]
                #chosenColor = min(max(chosenColor,0), 255)
                chosenColor = [int(chosenColor[0]), int(chosenColor[1]), int(chosenColor[2])]
                #print(chosenColor)
                return chosenColor
                

t = Tkinter.Tk()
a = App(t, terrain.grid)    
t.mainloop()
