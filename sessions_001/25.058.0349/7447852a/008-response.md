# 7447852a • 008 • example_2 • investigate_coder

---
```python
"""
Identify red pixels (value 2) in the input grid. For each row, fill the space between red pixels with yellow (value 4) up to 3 units away horizontally.
For each column, fill the space between red pixels with yellow (value 4) up to 3 units away vertically.
"""

import numpy as np

def get_red_pixels(grid):
    """
    Finds the coordinates of all red pixels in the grid.
    """
    red_pixels = []
    for row_idx, row in enumerate(grid):
        for col_idx, pixel in enumerate(row):
            if pixel == 2:
                red_pixels.append((row_idx, col_idx))
    return red_pixels

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    output_grid = np.copy(input_grid)
    red_pixels = get_red_pixels(input_grid)
    rows, cols = output_grid.shape
    
    # Horizontal filling
    for row_idx in range(rows):
        for i in range(len(red_pixels)):
            if red_pixels[i][0] == row_idx:
                #fill right
                for j in range(1,4):
                    if red_pixels[i][1] + j < cols:
                        if output_grid[row_idx, red_pixels[i][1] + j] == 0 or output_grid[row_idx, red_pixels[i][1] + j] == 2 :
                            output_grid[row_idx, red_pixels[i][1] + j] = 4
                #fill left
                for j in range(1,4):
                    if red_pixels[i][1] - j >= 0:
                        if output_grid[row_idx, red_pixels[i][1] - j] == 0 or output_grid[row_idx, red_pixels[i][1] - j] == 2:
                            output_grid[row_idx, red_pixels[i][1] - j] = 4
    # Vertical filling
    for col_idx in range(cols):
         for i in range(len(red_pixels)):
            if red_pixels[i][1] == col_idx:
                #fill down
                for j in range(1,4):
                    if red_pixels[i][0] + j < rows:
                         if output_grid[red_pixels[i][0] + j, col_idx] == 0 or output_grid[red_pixels[i][0] + j, col_idx] == 2:
                            output_grid[red_pixels[i][0] + j, col_idx] = 4
                #fill up
                for j in range(1,4):
                    if red_pixels[i][0] - j >= 0:
                        if output_grid[red_pixels[i][0] - j, col_idx] == 0 or output_grid[red_pixels[i][0] - j, col_idx] == 2:
                            output_grid[red_pixels[i][0] - j, col_idx] = 4


    return output_grid
```

