```python
"""
The transformation rule can be described as: all inner most pixels are removed, except:
    - Pixels on blocks with values: 3, 7, 8
    - If the block color is 9 and it surrounds a blue(1) it is transformed to 3
"""

import numpy as np

def is_inner_pixel(grid, i, j):
    """Checks if a pixel is an inner pixel of a block."""
    color = grid[i, j]
    if color == 0:  # Background, not inner
        return False

    neighbors = []
    for x in range(max(0, i - 1), min(grid.shape[0], i + 2)):
        for y in range(max(0, j - 1), min(grid.shape[1], j + 2)):
            if (x, y) != (i, j):
                neighbors.append(grid[x, y])
    
    return all(neighbor == color for neighbor in neighbors)

def transform(input_grid):
    """Transforms the input grid according to the specified rule."""

    input_grid = np.array(input_grid)  # Convert to NumPy array for easier manipulation
    output_grid = np.copy(input_grid)   # Initialize output_grid as a copy of the input_grid

    rows, cols = input_grid.shape

    # Iterate through each pixel in the input grid
    for i in range(rows):
        for j in range(cols):
            # Check if the pixel is an inner pixel
            if is_inner_pixel(input_grid, i, j):
                color = input_grid[i,j]
                if color in [4, 2, 6]:
                  output_grid[i,j] = 0
                if color == 9:
                    #find position of the 9 pixel
                    
                    #check neighbors to check if it contains a 1, if yes, change this 9 pixel to green
                    neighbors = []
                    
                    # collect all neighbors
                    for x in range(max(0, i - 1), min(input_grid.shape[0], i + 2)):
                        for y in range(max(0, j - 1), min(input_grid.shape[1], j + 2)):
                            if (x,y) != (i,j):
                                neighbors.append( (input_grid[x,y], (x, y)) )

                    is_next_to_1 = False
                    for neighbor_color, pos in neighbors:
                        if neighbor_color == 1:
                           is_next_to_1 = True
                           break

                    if is_next_to_1:
                        output_grid[i,j] = 3
                    else:
                        output_grid[i, j] = 0
            # else leave as is

    return output_grid.tolist()
```