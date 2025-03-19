# a48eeaf7 • 010 • example_2 • investigate_coder

---
```python
"""
Transforms the input grid by moving gray (5) pixels that are diagonally adjacent to a red (2) 2x2 square cluster. The gray pixels move one step closer to the center of the image either horizontally or vertically, but not both, based on their position relative to the red square.
"""

import numpy as np

def find_red_square(grid):
    # Find the top-left corner coordinates of the red square
    rows, cols = grid.shape
    for r in range(rows - 1):
        for c in range(cols - 1):
            if grid[r, c] == 2 and grid[r+1, c] == 2 and grid[r, c+1] == 2 and grid[r+1, c+1] == 2:
                return (r, c)  # Return top-left corner
    return None

def find_gray_pixels(grid):
    # Find coordinates of all gray pixels
    return np.argwhere(grid == 5)

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = input_grid.copy()
    
    # Find the top-left corner of the red square
    red_square_corner = find_red_square(input_grid)
    
    # Find all gray pixels
    gray_pixels = find_gray_pixels(input_grid)
    
    if red_square_corner is None:
        return output_grid

    red_r, red_c = red_square_corner
    
    # Iterate through gray pixels and move them
    for gray_r, gray_c in gray_pixels:
        # check if the gray pixel is to the left and above, above, or right and above the red square
        
        if (gray_r < red_r) and (gray_c < red_c or gray_c == red_c or gray_c == red_c + 1 or gray_c > red_c +1):
            # Move gray pixel down (increase row index)
            output_grid[gray_r, gray_c] = 0
            output_grid[gray_r + 1, gray_c] = 5
        elif (gray_r < red_r or gray_r == red_r or gray_r == red_r +1 or gray_r > red_r +1) and (gray_c < red_c):
            # move gray pixel to the right
            output_grid[gray_r, gray_c] = 0
            output_grid[gray_r, gray_c + 1] = 5
        elif (gray_r > red_r + 1) and (gray_c < red_c or gray_c == red_c or gray_c == red_c + 1 or gray_c > red_c + 1):
            #move gray pixel up
            output_grid[gray_r, gray_c] = 0
            output_grid[gray_r - 1, gray_c] = 5
        elif (gray_r < red_r or gray_r == red_r or gray_r == red_r + 1 or gray_r > red_r + 1) and (gray_c > red_c + 1):
             #move gray pixel to the left
            output_grid[gray_r, gray_c] = 0
            output_grid[gray_r, gray_c - 1] = 5

    return output_grid
```
