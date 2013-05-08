import math
import random

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
                
        def diamondSquare(self, x0 = 0, y0 = 0, x1 = 1, y1 = 1, roughness = 5, minHeight = 0, maxHeight = 1):
                heightRange = maxHeight - minHeight
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
                        maxDisplacement = 0.08 * heightRange
                        e = min(max(cornerAvg + random.uniform(-maxDisplacement, maxDisplacement), minHeight), maxHeight)
                        self.grid[midX][midY] = e
                        
                        # Square step
                        # Left
                        self.grid[x0][midY] = min(max(((a + c + e) / 3) + random.uniform(-maxDisplacement, maxDisplacement), minHeight), maxHeight)
                        # Above
                        self.grid[midX][y0] = min(max(((a + b + e) / 3) + random.uniform(-maxDisplacement, maxDisplacement), minHeight), maxHeight)
                        # Right
                        self.grid[x1][midY] = min(max(((b + d + e) / 3) + random.uniform(-maxDisplacement, maxDisplacement), minHeight), maxHeight)
                        # Below
                        self.grid[midX][y1] = min(max(((c + d + e) / 3) + random.uniform(-maxDisplacement, maxDisplacement), minHeight), maxHeight)

                        # Begin recursion..
                        # Upper left
                        self.diamondSquare(x0, y0, midX, midY, roughness, minHeight, maxHeight)
                        # Upper Right
                        self.diamondSquare(midX, y0, x1, midY, roughness, minHeight, maxHeight)
                        # Lower Left
                        self.diamondSquare(x0, midY, midX, y1, roughness, minHeight, maxHeight)
                        # Lower Right
                        self.diamondSquare(midX, midY, x1, y1, roughness, minHeight, maxHeight)

        def midpointDisplacement(self, x0, y0, x1, y1, roughness = 5, minHeight = 0, maxHeight = 1):
                heightRange = maxHeight - minHeight
                #print("Starting with coords:" + str([x0, y0, x1, y1]))
                maxIndex = len(self.grid)-1
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
                        maxDisplacement = (math.pow(2, roughness) / 255) * heightRange
                        #maxDisplacement = 0.1
                        e = min(max(((a + b + c + d) / 4) + random.uniform(-maxDisplacement, maxDisplacement), minHeight), maxHeight)
                        self.grid[halfwayX][halfwayY] = e                     
                        # Perform recursion
                        # Upper-left
                        self.midpointDisplacement(x0, y0, halfwayX, halfwayY, roughness, minHeight, maxHeight) 
                        # Upper-right
                        self.midpointDisplacement(halfwayX, y0, x1, halfwayY, roughness, minHeight, maxHeight)                              
                        # Lower-left
                        self.midpointDisplacement(x0, halfwayY, halfwayX, y1, roughness, minHeight, maxHeight)                              
                        # Lower-right
                        self.midpointDisplacement(halfwayX, halfwayY, x1, y1, roughness, minHeight, maxHeight)

        def seedIntervals(self, x0 = 0, y0 = 0, x1 = 1, y1 = 1, minHeight = 0, maxHeight = 1, subdivisions = 0, toroidal = False):
                if x1 - x0 > 1:
                        stepSize = int((x1 - x0) / subdivisions)
                        if stepSize > 0:
                                print("step: " + str(stepSize))
                                print("grid Dim: " + str(len(self.grid)))

                                # Seed values
                                for xSteps in range(subdivisions+1):
                                        for ySteps in range(subdivisions+1):
                                                self.grid[xSteps*stepSize][ySteps*stepSize] = min(max(random.uniform(minHeight, maxHeight), minHeight), maxHeight)

                                # In toroidal grid, north-south edges are identical, as are east-west                
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

        def seededDiamondSquare(self, x0, y0, x1, y1, minHeight, maxHeight, roughness, subdivisions, toroidal = False, fillSubGrids = True):
                subdivisions = int(math.pow(2, subdivisions))
                if x1 - x0 > 1:
                        stepSize = int((x1 - x0) / subdivisions)
                        if stepSize > 0:
                                # Generate height values for subgrid corners
                                self.seedIntervals(x0, y0, x1, y1, minHeight, maxHeight, subdivisions, toroidal)

                                # Perform midpoint displacement on subgrids
                                for xSteps in range(subdivisions):
                                        for ySteps in range(subdivisions):
                                                startX = xSteps*stepSize
                                                startY = ySteps*stepSize
                                                if fillSubGrids: self.diamondSquare(startX, startY, startX+stepSize, startY+stepSize, roughness, minHeight, maxHeight)
                        else:
                                print("Seeding of 'Diamond Square' failed: stepsize too small")
                                                

        def seededMidpointDisplacement(self, x0, y0, x1, y1, minHeight, maxHeight, roughness, subdivisions, toroidal = False, fillSubGrids = True):
                subdivisions = int(math.pow(2, subdivisions))
                if x1 - x0 > 1:
                        stepSize = int((x1 - x0) / subdivisions)
                        if stepSize > 0:
                                # Generate height values for subgrid corners
                                self.seedIntervals(x0, y0, x1, y1, minHeight, maxHeight, subdivisions, toroidal)

                                # Perform midpoint displacement on subgrids
                                for xSteps in range(subdivisions):
                                        for ySteps in range(subdivisions):
                                                startX = xSteps*stepSize
                                                startY = ySteps*stepSize
                                                if fillSubGrids: self.midpointDisplacement(startX, startY, startX+stepSize, startY+stepSize, roughness, minHeight, maxHeight)
                        else:
                                print("Seeding of 'Midpoint Displacement' failed: stepsize too small")
                                                

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
                                        
        def printGridTransposed(self):
                print("")
                for column in self.grid:
                        print(column)
                print("")
