import Tkinter as tk

class Map:
        def __init__(self, t, grid, windowDim, blockDim):
                self.i = tk.PhotoImage(width=windowDim, height=windowDim)
                self.c = tk.Canvas(t, width=windowDim, height=windowDim)
                self.c.pack()

                # Store grid information
                self.terrainGrid = grid
                self.windowDim = windowDim
                self.blockDim = blockDim

                # Track keypress offsets for map
                self.right = False
                self.left = False
                self.up = False
                self.down = False
                # Flag for whether map needs updating
                self.mapChanged = True
                # Track offset sizes
                self.xOffset = 0
                self.totalXOffset = 0
                self.yOffset = 0
                self.totalYOffset = 0
                # Navigation step size: 10% of grid width
                self.navStep = int(0.1 * len(self.terrainGrid))
                print("init navStep: " + str(self.navStep))

                # Calculate grid of colors
                useColors = True
                self.colorGrid = self.getColorGrid(self.terrainGrid, useColors)
                # Track canvas rectangles
                gridTotal = len(self.terrainGrid)*len(self.terrainGrid)
                self.rectangles = [x for x in range(gridTotal)]


        def updateCanvas(self):
                self.c.create_image(0, 0, image = self.i, anchor=tk.NW)
                self.c.update()

        def drawRects(self):
                gridDim = len(self.terrainGrid)
                useColors = True
                #colors = self.getColorGrid(self.terrainGrid, useColors)

                macroRow = 0; macroCol = 0              
                # Draw colors as rects
                count = 0
                print("Color grid len: " + str(len(self.colorGrid)))
                print("RectLen: " + str(len(self.rectangles)))
                for color in self.colorGrid:
                        # Get rect coords
                        x0 = macroCol * self.blockDim + self.xOffset
                        y0 = macroRow * self.blockDim + self.yOffset
                        x1 = x0 + self.blockDim
                        y1 = y0 + self.blockDim
                        # Draw Rect
                        strCol = '#%02x%02x%02x' % tuple(color)
                        # NOTE: Canvas coordinates start from bottom-left, so coordinates inverted to avoid terrain being transposed
                        rect = self.c.create_rectangle(y0, x0, y1, x1, outline = strCol, fill = strCol)
                        self.rectangles[count] = rect

                        #c.create_rectangle(x0, y0, x1, y1,  fill = strCol)

                        # Increment counters
                        macroCol += 1
                        # After last column of colours in row, move to start of next row
                        if macroCol == gridDim:
                                macroRow +=1; macroCol = 0
                        count += 1

        def updateRects(self):
                # Move every rectangle according to
                for rect in self.rectangles:
                        # Rect loc necessary to check for whether it is out of bounds
                        coords = self.c.coords(rect)

                        # Apply shifts
                        xShift = self.xOffset * self.blockDim
                        yShift = self.yOffset * self.blockDim
                        coords[0] += xShift
                        coords[2] += yShift

                        # Shift x coordinates
                        if coords[0] < 0:
                                xShift += self.windowDim
                        elif coords[0] >= self.windowDim:
                                xShift -= self.windowDim
                        # Shift y coordinates
                        if coords[1] < 0:
                                yShift += self.windowDim
                        elif coords[1] >= self.windowDim:
                                yShift -= self.windowDim
                        
                        self.c.move(rect, xShift, yShift)
                self.yOffset = 0
                self.xOffset = 0

        def updateMap(self, t):
                gridDim = len(self.terrainGrid)
                useColors = True
                #colors = self.getColorGrid(self.terrainGrid, useColors)

                macroRow = 0; macroCol = 0              
                if len(self.terrainGrid) == self.windowDim:
                        # Add pixels to canvas
                        for color in self.colorGrid:
                                for x in range(blockDim):
                                        for y in range(blockDim):
                                                adjustedX = (x + (self.xOffset * self.blockDim)) % gridDim
                                                adjustedY = (y + (self.yOffset * self.blockDim)) % gridDim
                                                row = (macroRow * self.blockDim) + adjustedY
                                                col = (macroCol * self.blockDim) + adjustedX
                                                rowString = str(macroRow) + "*" + str(self.blockDim) + "+" + str(adjustedY) + "=" + str(row)
                                                colString = str(macroCol) + "*" + str(self.blockDim) + "+" + str(adjustedX) + "=" + str(col)
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
                        for color in self.colorGrid:
                                # Get rect coords
                                x0 = macroCol * self.blockDim + self.xOffset
                                y0 = macroRow * self.blockDim + self.yOffset
                                x1 = x0 + self.blockDim
                                y1 = y0 + self.blockDim
                                # Draw Rect
                                strCol = '#%02x%02x%02x' % tuple(color)
                                # NOTE: Canvas coordinates start from bottom-left, so coordinates inverted to avoid terrain being transposed
                                self.c.create_rectangle(y0, x0, y1, x1, outline = strCol, fill = strCol)

                                #c.create_rectangle(x0, y0, x1, y1,  fill = strCol)

                                # Increment counters
                                macroCol += 1
                                # After last column of colours in row, move to start of next row
                                if macroCol == gridDim:
                                        macroRow +=1; macroCol = 0
                
        def getColorGrid(self, terrainGrid, useColors):
                gridDim = len(terrainGrid)
                colorGrid = []
                # Iterate over columns
                for x in range(gridDim):
                        # Iterate over rows
                        for y in range(gridDim):
                                #print("x + xOffset % gridDim, y + yOffset % gridDim")
                                #print(str(x) + " + " + str(self.xOffset) + " = "+ str((x+self.xOffset)%gridDim) + ", " + str(y) + " + " + str(self.yOffset) + " = "+ str((y+self.yOffset)%gridDim))
                                height = self.terrainGrid[(x+self.xOffset)%gridDim][(y+self.yOffset)%gridDim]
                                if useColors:
                                       color = self.getTerrainColor(height)
                                else:
                                        intensity = int(((height-minHeight)/maxHeight) * 255)
                                        color = [intensity for i in range(3)]
                                colorGrid.append(color)
                return colorGrid

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

        def applyKeyPressOffsets(self):
                # Apply keypress offsets
                if self.left:
                        self.xOffset += -self.navStep
                        self.resetKeys()
                elif self.right:
                        self.xOffset += self.navStep
                        self.resetKeys()
                if self.up:
                        self.yOffset += -self.navStep
                        self.resetKeys()
                elif self.down:
                        self.yOffset += self.navStep
                        self.resetKeys()

        def keyPressed(self, event):
                if event.keysym == 'Left':
                        self.left = True
                elif event.keysym == 'Right':
                        self.right = True
                elif event.keysym == 'Up':
                        self.up = True
                elif event.keysym == 'Down':
                        self.down = True
                self.mapChanged = True
                

        def resetKeys(self):
                self.up = False
                self.down = False
                self.left = False
                self.right = False
