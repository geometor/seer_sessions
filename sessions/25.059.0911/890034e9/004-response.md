# 890034e9 • 004 • example_1 • investigate_coder

---
```python
"""
Locate all red (2) squares in the input grid. For each identified red square, examine its interior. If the interior of a red square contains any white(0) pixels, change those white (0) pixels to red (2). Otherwise if there is a 1x1 red pixel at the center, do nothing. All other parts of the grid remain identical between input and output.
"""

import numpy as np

def find_squares(grid, color):
    # Find all pixels of the specified color.
    pixels = np.argwhere(grid == color)
    squares = []

    # Process each potential square starting point.
    processed = np.zeros_like(grid, dtype=bool)
    for p in pixels:
      r, c = p
      if not processed[r,c]:
        size = 0
        # check for the extent
        while r + size < grid.shape[0] and c + size < grid.shape[1] and grid[r + size, c] == color and grid[r, c + size] == color:
                size +=1

        # all cells are same color
        is_square = True
        for i in range(r,r+size):
            for j in range(c, c+size):
                if grid[i,j] != color:
                    is_square = False
                    break
            if not is_square:
                break
        
        if is_square and size>0:
            squares.append((r,c,size))
            processed[r:r+size, c:c+size] = True

    return squares

def get_interior(grid, r, c, size):
    # Extract the interior of a square, excluding its border.
    return grid[r+1:r+size-1, c+1:c+size-1]

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    
    # Find all red squares
    red_squares = find_squares(output_grid, 2)

    # Iterate through each red square
    for r, c, size in red_squares:
        # Get the interior of the square
        interior = get_interior(output_grid, r, c, size)
        
        # Check if the interior contains white pixels
        if interior.size > 0 and np.any(interior == 0):  # Check if interior exists and contains white (0)
            # Replace white pixels in the interior with red
            output_grid[r+1:r+size-1, c+1:c+size-1][interior == 0] = 2

    return output_grid
```
