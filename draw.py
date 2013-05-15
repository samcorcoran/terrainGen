import Tkinter as tk

class Map:
	def __init__(self, t, terrain, windowDim, blockDim):
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

                # Shadowing
                self.useShadows = True
                self.minHeightForShadows = 0
                self.occlusionSteps = 3
		self.xOccluderDir = 1
		self.yOccluderDir = 0
		self.occlusionHeight = 0.01
		# Calculate grid of colors
		self.useColors = True
		self.interpColorAcrossBands = False
		self.colorGrid = self.getColorGrid()
		# Track canvas rectangles
		self.rectangles = []

	# Redraw canvas
	def updateCanvas(self):
		self.c.update()

	# Create canvas rectangles of correct dimensions and starting locations
	def createRects(self):
		gridDim = len(self.terrain.grid)
		macroRow = 0; macroCol = 0              
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
			rect = self.c.create_rectangle(y0, x0, y1, x1, outline = strCol, fill = strCol)
			self.rectangles.append(rect)

			# Increment counters
			macroCol += 1
			# After last column of colours in row, move to start of next row
			if macroCol == gridDim:
				macroRow +=1; macroCol = 0
				#break

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
		
	def getColorGrid(self):
		gridDim = len(self.terrain.grid)
		colorGrid = []
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
				colorGrid.append(color)
		return colorGrid

	def getTerrainColor(self, height, x, y):
		# Height proportions at which different terrain colors end
		height *= 255
		
		# In-land hills and mountains colouring
		#self.minHeightForShadows = 0.15
		#seaLevel = 0.15 * 255
		#sandLevel = 0.2 * 255
		#grassLevel = 0.55 * 255
		#hillLevel = 0.75 * 255
		#mountainLevel = 0.9 * 255
		
		# Island colouring
		self.minHeightForShadows = 0.65
		seaLevel = 0.65 * 255
		sandLevel = 0.68 * 255
		grassLevel = 0.85 * 255
		hillLevel = 0.92 * 255
		mountainLevel = 0.98 * 255
		
		if height < seaLevel:
			seaMin = 50
			seaMax = 140
			t = 0.5
			if self.interpColorAcrossBands:
				t = height/seaLevel
			c = seaMin + t*(seaMax-seaMin)
			chosenColor = [0, 0, c]
		elif height < sandLevel:
			sandMin = 75
			sandMax = 125
			# Interpolation is reversed so low-sand is light green and high-grass is dark green
			t = 0.5
			if self.interpColorAcrossBands:
				t = 1-((height-seaLevel)/(sandLevel-seaLevel))
			c = sandMin + t*(sandMax-sandMin)
			chosenColor = [c, c, 0]
			#chosenColor = [255, 0, 0]
		elif height < grassLevel:
			grassMin = 30
			grassMax = 80
			t = 0.5
			if self.interpColorAcrossBands:
				# Interpolation is reversed so low-grass is light green and high-grass is dark green
				t = 1-((height-sandLevel)/(grassLevel-sandLevel))
			c = grassMin + t*(grassMax-grassMin)
			chosenColor = [0, c, 0]
		elif height < hillLevel:
			hillMin = 30
			hillMax = 55
			t = 0.5
			if self.interpColorAcrossBands:
				t = ((height-grassLevel)/(hillLevel-grassLevel))
			c = hillMin + t*(hillMax-hillMin)                        
			chosenColor = [c, c, 0]
		elif height < mountainLevel:
			mountainMin = 60
			mountainMax = 170
			t = 0.5
			if self.interpColorAcrossBands:
				t = ((height-hillLevel)/(mountainLevel-hillLevel))
			c = mountainMin + t*(mountainMax-mountainMin)                        
			chosenColor = [c, c, c]
		else:
			snowMin = 200
			snowMax = 255
			t = 0.5
			if self.interpColorAcrossBands:
				t = ((height-mountainLevel)/(1-mountainLevel))
			c = snowMin + t*(snowMax-snowMin)
			chosenColor = [c, c, c]

		# Ensure integer values for colors
		chosenColor = [int(chosenColor[0]), int(chosenColor[1]), int(chosenColor[2])]

		# Apply shadowing
		if self.useShadows:
                        shadowing = 1 - self.getLocShadowing(x, y)
                        chosenColor[0] = int(chosenColor[0] * shadowing)
                        chosenColor[1] = int(chosenColor[1] * shadowing)
                        chosenColor[2] = int(chosenColor[2] * shadowing)
		
		return chosenColor

	def getLocShadowing(self, x, y):
		# Check location is on-grid
		shadowed = False
		shadowing = 0
		##print("Checking shadows for " + str((x,y)) + " (height = "+str(thisHeight)+"):")
		if x >= 0 and x < self.windowDim:
			if y >= 0 and y < self.windowDim:
                         	thisHeight = self.terrain.grid[x][y]
                         	# Terrain below min shadow height is unaffected
                                if thisHeight >= self.minHeightForShadows:
                                        # StepsTaken measured so nearby occluders can block more light
                                        # Check occlusion in direction of light source
                                        stepsTaken = self.isLocShadowedByDir(x, y, self.xOccluderDir, self.yOccluderDir, self.occlusionSteps)
                                        shadowing += 0.2 * stepsTaken/self.occlusionSteps
                                        # Check occlusion orthogonal to direction of light source
                                        stepsTaken = self.isLocShadowedByDir(x, y, -self.xOccluderDir, self.yOccluderDir, self.occlusionSteps)
                                        shadowing += 0.1 * stepsTaken/self.occlusionSteps
                                        stepsTaken = self.isLocShadowedByDir(x, y, self.xOccluderDir, -self.yOccluderDir, self.occlusionSteps)
                                        shadowing += 0.1 * stepsTaken/self.occlusionSteps
		return shadowing

        # Returns 0 if no occlusion, otherwise number of steps to occluder
	def isLocShadowedByDir(self, x, y, xOccDir, yOccDir, steps):
		thisHeight = self.terrain.grid[x][y]
		stepsTaken = 0
		for step in range(1, steps+1):
			occX = (x + (xOccDir * (step + 1))) % len(self.terrain.grid)
			occY = (y + (yOccDir * (step + 1))) % len(self.terrain.grid)
			if self.terrain.grid[occX][occY] >= thisHeight + self.occlusionHeight:
                                stepsTaken = steps
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
