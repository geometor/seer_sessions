# 3906de3d • 002 • example_3 • investigate_coder

---
```python
"""
1.  **Identify Objects:** Locate the contiguous blue object and the contiguous red object within the input grid. Note the shape and position of both.
2.  **Transfer Property:** Transfer "redness" to any blue pixel directly above a red pixel. The red pixels from the blue object should replace the lowest blue pixels that are immediately "above", the original red pixels, in the corresponding input column.
3.  **Remove Source object:** The separate red object at the bottom is removed in the output.

In essence, the red object "projects" its shape upwards onto the blue object, replacing some of the blue pixels with red ones, and then disappears. The background remains unchanged.
"""

import numpy as np

def find_object(grid, color):
    """Finds the coordinates of an object of the specified color."""
    coords = []
    for r, row in enumerate(grid):
        for c, pixel in enumerate(row):
            if pixel == color:
                coords.append((r, c))
    return coords

def get_contiguous_block(grid, start_coord, color):
    """Gets a contiguous block of pixels of a given color, starting from a given coordinate."""

    rows, cols = len(grid), len(grid[0])
    visited = set()
    block = []
    queue = [start_coord]

    while queue:
        r, c = queue.pop(0)
        if (r, c) in visited:
            continue
        visited.add((r, c))

        if not (0 <= r < rows and 0 <= c < cols) or grid[r][c] != color:
            continue
        
        block.append((r,c))

        # Add neighbors to the queue
        queue.append((r - 1, c))  # Up
        queue.append((r + 1, c))  # Down
        queue.append((r, c - 1))  # Left
        queue.append((r, c + 1))  # Right

    return block
    

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    grid = np.array(input_grid)
    output_grid = np.copy(grid)
    
    # Find the blue and red objects
    blue_coords = find_object(grid, 1)
    # handle cases where no blue/red object by checking the length of the return value
    if (len(blue_coords) > 0):
        blue_object = get_contiguous_block(grid, blue_coords[0], 1)
    else:
        blue_object = []
    
    red_coords = find_object(grid, 2)
    if (len(red_coords) > 0):
        red_object = get_contiguous_block(grid, red_coords[0], 2)
    else:
        red_object = []

    # Create a dictionary to store the lowest blue pixel's row index for each column.
    lowest_blue_in_column = {}
    for r, c in blue_object:
        if c not in lowest_blue_in_column or r > lowest_blue_in_column[c]:
              lowest_blue_in_column[c] = r

    # Transfer redness
    for r, c in red_object:
        if c in lowest_blue_in_column:
            output_grid[lowest_blue_in_column[c]][c] = 2

    # remove the red object
    for r,c in red_object:
        output_grid[r][c] = 0


    return output_grid.tolist()
```
