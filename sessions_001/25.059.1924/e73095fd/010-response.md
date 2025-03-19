# e73095fd • 010 • example_2 • investigate_coder

---
```python
"""
The transformation identifies a closed shape formed by gray (5) pixels and fills its interior with yellow (4) pixels, leaving the rest of the grid unchanged.
"""

import numpy as np
from scipy.ndimage import label, measurements

def find_objects(grid, color):
    """Finds connected regions of the specified color."""
    binary_grid = (grid == color).astype(int)
    labeled_grid, num_objects = label(binary_grid)
    return labeled_grid, num_objects

def is_inside(labeled_grid, object_id, grid_shape):
    """Checks if an object is completely enclosed by boundary pixels."""
    rows, cols = grid_shape
    object_pixels = np.where(labeled_grid == object_id)

    # Check if any object pixel is on the edge of the grid
    if any(object_pixels[0] == 0) or any(object_pixels[0] == rows - 1) or \
       any(object_pixels[1] == 0) or any(object_pixels[1] == cols - 1):
        return False

    return True

def transform(input_grid):
    """Fills the interior of a closed shape formed by '5' pixels with '4'."""
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find boundary objects (color 5)
    boundary_labeled_grid, num_boundary_objects = find_objects(input_grid, 5)

    # Find background objects (color 0)
    background_labeled_grid, num_background_objects = find_objects(input_grid, 0)
    
    # Iterate through background objects
    for obj_id in range(1, num_background_objects + 1):
        # check if they are inside
        if is_inside(background_labeled_grid, obj_id, (rows, cols)):
            # Get the coordinates of the background object
            coords = np.where(background_labeled_grid == obj_id)

            # check neighbors
            is_enclosed = True
            for r, c in zip(*coords):
                neighbors = []
                if r > 0:
                    neighbors.append(input_grid[r-1, c])
                if r < rows - 1:
                    neighbors.append(input_grid[r+1, c])
                if c > 0:
                    neighbors.append(input_grid[r, c-1])
                if c < cols - 1:
                    neighbors.append(input_grid[r, c+1])
                if not all(n == 5 or n == 0 for n in neighbors):
                    is_enclosed=False
                    break
                
            if is_enclosed:          
                # flood fill
                pixels_to_fill = [(r,c) for r,c in zip(*coords)]
                visited = set()

                while pixels_to_fill:
                  r,c = pixels_to_fill.pop()
                  
                  if (r,c) in visited or input_grid[r,c] != 0:
                    continue

                  visited.add((r,c))
                  output_grid[r,c] = 4 # set color to yellow

                  if r > 0 :
                    pixels_to_fill.append((r-1,c))
                  if r < rows-1:
                    pixels_to_fill.append((r+1,c))
                  if c > 0 :
                    pixels_to_fill.append((r,c-1))
                  if c < cols -1:
                    pixels_to_fill.append((r,c+1))

    return output_grid
```
