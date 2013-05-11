import tkinter

class Map:
        def __init__(self, t, terrainGrid, windowDim, blockDim=1):
                gridDim = len(terrainGrid)
            
                self.i = tkinter.PhotoImage(width=windowDim, height=windowDim)
            
                useColors = True
                colors = []
                # Iterate over columns
                for x in range(gridDim):
                        # Iterate over rows
                        for y in range(gridDim):
                                height = terrainGrid[x][y]
                                if useColors:
                                        color = self.getTerrainColor(height)
                                else:
                                        intensity = int(((height-minHeight)/maxHeight) * 255)
                                        color = [intensity for i in range(3)]
                                colors.append(color)

                c = tkinter.Canvas(t, width=windowDim, height=windowDim); c.pack()

                macroRow = 0; macroCol = 0              
                if len(terrainGrid) == windowDim:
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
                c.create_image(0, 0, image = self.i, anchor=tkinter.NW)

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
