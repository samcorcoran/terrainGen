import Tkinter as tk

class Map:
	def __init__(self, t, terrain, windowDim, blockDim, flatSea):
		self.i = tk.PhotoImage(width=windowDim, height=windowDim)
		self.c = tk.Canvas(t, width=windowDim, height=windowDim)
		self.c.pack()

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
		# Navigation step size: 10% of grid width
		self.navStep = int(0.1 * len(self.terrain.grid))
		print("init navStep: " + str(self.navStep))

                # Render all sea as a single tile underneath land tiles
                self.flatSea = flatSea

		# Color bands (terrain height cut offs, e.g. 0.65 seaLevel means that heights below 0.65 are sea)
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

                # Shadowing
                self.useShadows = True
                self.shadowStrength = 0.2
                self.minHeightForShadows = 0
                self.occlusionSteps = 5
		self.xOccluderDir = 1
		self.yOccluderDir = 0
		self.occlusionHeight = 0
		# Calculate grid of colors
		self.useColors = True
		self.interpColorAcrossBands = True
		self.colorGrid2d = self.getColorGrid2D()

		# Track canvas rectangles
		self.rectangles = []

	# Redraw canvas
	def updateCanvas(self):
		self.c.update()

	# Create canvas rectangles of correct dimensions and starting locations
	def createRects(self):
                # Flat sea is a single window-wide tile
                if self.flatSea:
               		strCol = '#%02x%02x%02x' % (0, 0, 80)
                        seaRect = self.c.create_rectangle(0, 0, self.windowDim, self.windowDim, outline = strCol, fill = strCol)
                
		gridDim = len(self.terrain.grid)
		macroRow = 0; macroCol = 0              
		# Draw colors as rects
		for row in range(gridDim):
                        for col in range(gridDim):
                                # If terrain is above sea level, create tile
                                if not self.flatSea or self.terrain.grid[row][col] > 0.65:
                                        # Get rect coords
                                        x0 = col * self.blockDim + self.xOffset
                                        y0 = row * self.blockDim + self.yOffset
                                        x1 = x0 + self.blockDim
                                        y1 = y0 + self.blockDim

                                        color = self.colorGrid2d[row][col]
                                        # Draw Rect
                                        strCol = '#%02x%02x%02x' % tuple(color)
                                        # NOTE: Canvas coordinates start from bottom-left, so coordinates inverted to avoid terrain being transposed
                                        rect = self.c.create_rectangle(y0, x0, y1, x1, outline = strCol, fill = strCol)
                                        self.rectangles.append(rect)
                print("Total rects: " + str(len(self.rectangles)))

	# Moves tile rectangles according to x and y offset values
	def updateRects(self):
		for rect in self.rectangles:
			# Rect loc necessary to check for whether it is out of bounds
			coords = self.c.coords(rect)

			# Apply shifts
			xShift = self.xOffset * self.blockDim
			yShift = self.yOffset * self.blockDim
			coords[0] += xShift
			coords[1] += yShift

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
					# Perform move call on rectangle
			#print("Rectangle " + str(rect) + " has coords: " + str(coords) + " and shifts: " + str(xShift) + " " + str(yShift))						
			self.c.move(rect, xShift, yShift)
		self.yOffset = 0
		self.xOffset = 0

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


	def getTerrainColor(self, height, x, y):
		# Height proportions at which different terrain colors end
		height *= 255

		seaLevelCol = self.seaLevel * 255
		sandLevelCol = self.sandLevel * 255
		grassLevelCol = self.grassLevel * 255
		hillLevelCol = self.hillLevel * 255
		mountainLevelCol = self.mountainLevel * 255

		if height < seaLevelCol:
			seaMin = 50
			seaMax = 140
			t = 0.5
			if self.interpColorAcrossBands:
				t = height/seaLevelCol
			c = seaMin + t*(seaMax-seaMin)
			chosenColor = [0, 0, c]
		elif height < sandLevelCol:
			sandMin = 75
			sandMax = 125
			# Interpolation is reversed so low-sand is light green and high-grass is dark green
			t = 0.5
			if self.interpColorAcrossBands:
				t = 1-((height-seaLevelCol)/(sandLevelCol-seaLevelCol))
			c = sandMin + t*(sandMax-sandMin)
			chosenColor = [c, c, 0]
			#chosenColor = [255, 0, 0]
		elif height < grassLevelCol:
			grassMin = 30
			grassMax = 80
			t = 0.5
			if self.interpColorAcrossBands:
				# Interpolation is reversed so low-grass is light green and high-grass is dark green
				t = 1-((height-sandLevelCol)/(grassLevelCol-sandLevelCol))
			c = grassMin + t*(grassMax-grassMin)
			chosenColor = [0, c, 0]
		elif height < hillLevelCol:
			hillMin = 30
			hillMax = 55
			t = 0.5
			if self.interpColorAcrossBands:
				t = ((height-grassLevelCol)/(hillLevelCol-grassLevelCol))
			c = hillMin + t*(hillMax-hillMin)                        
			chosenColor = [c, c, 0]
		elif height < mountainLevelCol:
			mountainMin = 60
			mountainMax = 170
			t = 0.5
			if self.interpColorAcrossBands:
				t = ((height-hillLevelCol)/(mountainLevelCol-hillLevelCol))
			c = mountainMin + t*(mountainMax-mountainMin)                        
			chosenColor = [c, c, c]
		else:
			snowMin = 200
			snowMax = 255
			t = 0.5
			if self.interpColorAcrossBands:
				t = ((height-mountainLevelCol)/(1-mountainLevelCol))
			c = snowMin + t*(snowMax-snowMin)
			chosenColor = [c, c, c]

		# Ensure integer values for colors
		chosenColor = [int(chosenColor[0]), int(chosenColor[1]), int(chosenColor[2])]

		# Apply shadowing
		if self.useShadows:
                        shadowing = min((1 - self.getLocShadowing(x, y)) * (1-self.shadowStrength), 1)
                        chosenColor[0] = int(chosenColor[0] * shadowing)
                        chosenColor[1] = int(chosenColor[1] * shadowing)
                        chosenColor[2] = int(chosenColor[2] * shadowing)
		
		return chosenColor

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
