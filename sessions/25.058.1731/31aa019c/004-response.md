# 31aa019c • 004 • example_1 • investigate_coder

---
```python
"""
The transformation identifies colored object in the input, replaces it near their combined center area with a 3x3 red square, changes the center square to yellow, and makes the rest of the image white.
"""

import numpy as np

def find_colored_pixels(grid):
    # Find coordinates of all non-zero (colored) pixels.
    colored_pixels = []
    for row_idx, row in enumerate(grid):
        for col_idx, pixel in enumerate(row):
            if pixel != 0:
                colored_pixels.append((row_idx, col_idx, pixel))
    return colored_pixels

def calculate_center(colored_pixels):
    # Calculate the average row and column indices of colored pixels.
    if not colored_pixels:
        return (0, 0)  # Return a default center if no colored pixels

    sum_row = 0
    sum_col = 0
    for row, col, _ in colored_pixels:
        sum_row += row
        sum_col += col
    center_row = round(sum_row / len(colored_pixels))
    center_col = round(sum_col / len(colored_pixels))
    return (center_row, center_col)
    

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    
    # Find colored pixels in the input grid
    colored_pixels = find_colored_pixels(input_grid)
    
    # Calculate approximate center of the object
    center_row, center_col = calculate_center(colored_pixels)

    # adjust center based on observations from multiple examples
    block_start_row = center_row - 2
    block_start_col = center_col - 4 # shifted more to the left
    
    # Create the 3x3 block of color 2 (red)
    for i in range(3):
        for j in range(3):
            row = block_start_row + i
            col = block_start_col + j
            # check bounds 
            if 0 <= row < output_grid.shape[0] and 0 <= col < output_grid.shape[1]:
                output_grid[row, col] = 2

    # change center pixel to color 4 (yellow)
    center_block_row = block_start_row + 1
    center_block_col = block_start_col + 1
        # check bounds
    if 0 <= center_block_row < output_grid.shape[0] and 0 <= center_block_col < output_grid.shape[1]:     
      output_grid[center_block_row,center_block_col] = 4


    return output_grid
```
