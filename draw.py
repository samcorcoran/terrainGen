import pyglet
from pyglet.gl import *
from pyglet.window import key

import tile

class MapWindow(pyglet.window.Window):
    def __init__(self, terrain, windowDim, blockDim, flatSea):
        super(MapWindow, self).__init__(fullscreen=False, caption='TerrainGen Map')

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        self.set_size(windowDim, windowDim)

        # Store grid information
        self.terrain = terrain
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
        # Navigation step size: 10% of grid width, minimum of 1
        self.navStep = max(1, int(0.1 * len(self.terrain.grid)))
        self.navStepMultiplier = 3
        print("init navStep: " + str(self.navStep) + " (multiplier: " + str(self.navStepMultiplier) + ")")

        # Render all sea as a single tile underneath land tiles
        self.flatSea = flatSea
        self.flatSeaHeight = 0.65
        self.flatSeaColor = (0, 0, 0.25)
        #pyglet.gl.glClearColor(self.flatSeaColor[0], self.flatSeaColor[1], self.flatSeaColor[2], 1)

        # Shadowing
        self.useShadows = False
        self.shadowStrength = 0.2
        self.minHeightForShadows = 0
        self.occlusionSteps = 5
        self.xOccluderDir = 1
        self.yOccluderDir = 0
        self.occlusionHeight = 0
        # Calculate grid of colors
        self.useColors = True
        self.interpColorAcrossBands = True
        #self.colorGrid2d = self.getColorGrid2D()

        # Track bottom-left coordinates of tiles
        self.tiles = []

    #@window.event
    def on_draw(self):
        self.clear()
        # If required, draw baseline water
        self.drawFlatSea()
        # Draw terrain tiles
        pyglet.gl.glColor4f(1.0,0,0,1.0)
        #print("Total terrain tiles:" + str(len(self.tiles)))
        self.drawTiles()

    def drawTiles(self):
        for tile in self.tiles:
            #tile.printTile()
            self.drawTile(tile)

    # Draws a tile based on data in object
    def drawTile(self, tile):
        # Apply shifts
        xShift = self.xOffset
        yShift = self.yOffset

        x0 = tile.xLoc + xShift
        y0 = tile.yLoc + yShift

        # Adjust locations if offsets resulted in out-of-bounds
        # Shift x coordinates
        if x0 < 0:
            x0 += self.windowDim
        elif x0 + tile.length > self.windowDim:
            x0 -= self.windowDim
        # Shift y coordinates
        if y0 < 0:
            y0 += self.windowDim
        elif y0 + tile.length > self.windowDim:
            y0 -= self.windowDim

        self.drawSquare(x0, y0, tile.length, tile.color)

    # Draw a single rectangle behind terrain colored as sea
    def drawFlatSea(self):
        # Draw flat sea
        if self.flatSea:
            #print("Flat sea top coord: " + str(self.terrain.xDim * self.blockDim))
            self.drawSquare(0, 0, self.terrain.xDim * self.blockDim, self.flatSeaColor)

    def drawSquare(self, x0, y0, height, color):
        # Set square colour
        pyglet.gl.glColor4f(color[0], color[1], color[2], 1.0)
        # Draw tile as two triangles
        pyglet.graphics.draw_indexed(4, pyglet.gl.GL_TRIANGLES,
            [0, 1, 2, 0, 2, 3],
            ('v2i', (x0, y0,
                x0+height, y0,
                x0+height, y0+height,
                x0, y0+height))
        )

    # Redraw canvas
    def updateCanvas(self):
        self.c.update()

    # Create tiles of correct dimensions and starting locations
    def createTiles(self):
        # Flat sea is a single window-wide tile
        print("Creating tiles...")
        gridDim = self.terrain.xDim
        macroRow = 0; macroCol = 0              
        # Draw colors as tiles
        for row in range(gridDim):
            for col in range(gridDim):
                # If terrain is above sea level, create tile
                if not self.flatSea or self.terrain.grid[row][col] > self.flatSeaHeight:
                    # Get tile coords
                    x0 = col * self.blockDim
                    y0 = row * self.blockDim
                    x1 = x0 + self.blockDim
                    y1 = y0 + self.blockDim

                    #color = self.colorGrid2d[row][col]

                    newTile = tile.Tile(x0, y0, self.blockDim, self.terrain.grid[row][col])
                    newTile.calculateTerrainColor(self.useColors, self.interpColorAcrossBands)
                    self.tiles.append(newTile)

        print("Total tiles: " + str(len(self.tiles)))

    def getColorGrid2D(self):
        gridDim = len(self.terrain.grid)
        colorGrid2d = [[1 for x in range(gridDim)] for y in range(gridDim)]
        # Iterate over columns
        for x in range(gridDim):
            # Iterate over rows
            for y in range(gridDim):
                #print("x + xOffset % gridDim, y + yOffset % gridDim")
                #print(str(x) + " + " + str(self.xOffset) + " = "+ str((x+self.xOffset)%gridDim) + ", " + str(y) + " + " + str(self.yOffset) + " = "+ str((y+self.yOffset)%gridDim))
                xLoc = (x+self.xOffset)%gridDim
                yLoc = (y+self.yOffset)%gridDim
                height = self.terrain.grid[xLoc][yLoc]
                if self.useColors:
                       color = self.getTerrainColor(height, xLoc, yLoc)
                else:
                    intensity = int(((height-self.terrain.minHeight)/self.terrain.maxHeight) * 255)
                    color = [intensity for i in range(3)]
                colorGrid2d[x][y] = color
        return colorGrid2d

    # Larger shadowing numbers indicate deeper shadows
    def getLocShadowing(self, x, y):
        # Check location is on-grid
        shadowed = False
        shadowing = 0.0
        ##print("Checking shadows for " + str((x,y)) + " (height = "+str(thisHeight)+"):")
        if x >= 0 and x < self.windowDim:
            if y >= 0 and y < self.windowDim:
                thisHeight = self.terrain.grid[x][y]
                # Terrain below min shadow height is unaffected
                if thisHeight >= self.minHeightForShadows:
                    # StepsTaken measured so nearby occluders can block more light
                    # Check occlusion in direction of light source
                    stepsTaken = self.isLocShadowedByDir(x, y, self.xOccluderDir, self.yOccluderDir, self.occlusionSteps)
                    if stepsTaken > 0:
                            shadowing += 0.07 * self.occlusionSteps/stepsTaken
                    # Check occlusion orthogonal to direction of light source
                    stepsTaken = self.isLocShadowedByDir(x, y, -self.xOccluderDir, self.yOccluderDir, self.occlusionSteps)
                    if stepsTaken > 0:
                            shadowing += 0.007 * self.occlusionSteps/stepsTaken
                    stepsTaken = self.isLocShadowedByDir(x, y, self.xOccluderDir, -self.yOccluderDir, self.occlusionSteps)
                    if stepsTaken > 0:
                            shadowing += 0.007 * self.occlusionSteps/stepsTaken
        return shadowing

        # Returns 0 if no occlusion, otherwise number of steps to occluder
    def isLocShadowedByDir(self, x, y, xOccDir, yOccDir, steps):
        thisHeight = self.terrain.grid[x][y]
        stepsTaken = 0
        for step in range(1, steps+1):
            occX = (x + (xOccDir * (step + 1))) % len(self.terrain.grid)
            occY = (y + (yOccDir * (step + 1))) % len(self.terrain.grid)
            if self.terrain.grid[occX][occY] >= thisHeight + self.occlusionHeight:
                stepsTaken = step
                break
        return stepsTaken
    
    def applyKeyPressOffsets(self):
        # Apply keypress offsets
        if self.left:
            self.xOffset += -self.navStep * self.blockDim
            self.resetKeys()
        elif self.right:
            self.xOffset += self.navStep * self.blockDim
            print("Right offsetting by " + str(self.navStep) + " * " + str(self.blockDim))
            self.resetKeys()
        if self.up:
            self.yOffset += self.navStep * self.blockDim
            self.resetKeys()
        elif self.down:
            self.yOffset += -self.navStep * self.blockDim
            self.resetKeys()
        
        # Keep offsets between +/- self.windowDim
        self.xOffset %= self.windowDim
        self.yOffset %= self.windowDim

        print("xOffset: " + str(self.xOffset))
        print("yOffset: " + str(self.yOffset))

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

    #@window.event
    def on_key_press(self, symbol, modifiers):
        if symbol == key.A:
            print("The 'A' key was pressed.")
        elif symbol == key.LEFT:
            print("The left arrow key was pressed.")
            self.left = True
        elif symbol == key.RIGHT:
            print("The right arrow key was pressed.")
            self.right = True
        elif symbol == key.UP:
            print("The up arrow key was pressed.")
            self.up = True
        elif symbol == key.DOWN:
            print("The down arrow key was pressed.")
            self.down = True
        elif symbol == key.ENTER:
            print("The enter key was pressed.")
        self.applyKeyPressOffsets()