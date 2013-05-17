terrainGen
==========

A python experiment in procedural terrain generation.

## How To Run

Running main.py will generate a heightmap and render it using python's TKinter. 

Parameters are currently hard-coded, but can be edited to change the manner of generation.

## Implemented Modes

### Diamond Square

* Corners are initialised with random height values
* Grid midpoint calculated from average plus a random displacement
* Edge midpoints calculated from average of neighbouring corners and recently generated midpoint
* Recursively solves sub-grids

### Midpoint Displacement

* Corners are initialised with random height values
* Grid edge midpoints are calculated from pairs of corners plus random displacements.
* Grid central midpoint calculated from average of edge midpoints
* Recursively solves sub-grids

## Additional Sub-Modes/Features

### Terrain Smoothing

Every grid location becomes the average of itself and neighbours. Neighbourhood/kernel size is based on grid size, while number of repeated smoothing iterations can be controlled.

### Sub-grid Initialisation

Pre-initialised corners are generated for a series of sub-grids, which are then separately solved. Shared corner values allow for smooth transitions between sub-grids.

### Toroidal Generation

Any pre-initialised corner values on north boundary are duplicated on south boundary. East-West boundaries are also duplicates. This allows seamless generation over map boundaries, creating a toroidal landscape.
