```python
"""
1.  **Identify Objects:** Locate all contiguous blocks of pixels with the color red (2) and azure (8).
2.  **Find Adjacency:** For each red block, determine if there's an adjacent azure block. Adjacency includes directly above, below, left, or right, not diagonal.
3.  **Duplicate and Transform:**
    *    Iterate through cells in the input grid.
    *   If the current cell is Red(2):
        *   Extend/duplicate the Red colored object towards any immediately adjacent azure object by filling the path between them with red pixels.
        *   Change one of the duplicated red pixel nearest to color 8 to yellow (4)
4. **Output:** Return the modified grid.
"""

import numpy as np

def find_objects(grid, color):
    """Finds the coordinates of all pixels of a given color."""
    objects = []
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color:
                objects.append((r, c))
    return objects

def closest_object(grid, start_coords, target_color):
     """Finds the closest object of the target color, and returns the path"""
     rows, cols = grid.shape
     min_dist = float('inf')
     closest_coord = None

     target_coords = find_objects(grid, target_color)

     for target in target_coords:
        dist = abs(target[0] - start_coords[0]) + abs(target[1] - start_coords[1])
        if dist < min_dist:
            min_dist = dist
            closest_coord = target

     if closest_coord == None:
          return None, None

     # determine path
     path = []
     r, c = start_coords
     tr, tc = closest_coord

     if r != tr: # move vertically
        step = 1 if tr > r else -1
        for i in range(r, tr, step):
             path.append( (i,c))

     if c != tc: #move horizonally
        step = 1 if tc > c else -1
        for i in range(c, tc, step):
             path.append( (r,i))
             
     #return path including start
     return closest_coord, path

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Identify red and azure objects
    red_objects = find_objects(output_grid, 2)

    if not red_objects: # Handle cases where no Red is present.
        return output_grid

    # Find adjacency and duplicate
    for red_coord in red_objects:

        closest_azure, path = closest_object(output_grid, red_coord, 8)
        
        if closest_azure != None and path!=None:

          for coord in path:
              output_grid[coord]=2 #duplicate color

          # change to yellow
          if len(path)>0:
            #find closest point in the path
            min_dist = float('inf')
            closest_to_azure = None

            for p in path:
              dist = abs(p[0]- closest_azure[0]) + abs(p[1]- closest_azure[1])
              if dist<min_dist:
                min_dist = dist
                closest_to_azure= p

            output_grid[closest_to_azure]=4

    return output_grid
```