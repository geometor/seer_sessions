# 22233c11 • 004 • example_1 • investigate_coder

---
```python
"""
1.  **Identify Green Pixels:** Locate all pixels in the input grid that are colored green (value 3).
2.  **Check for diagonal pairs:** see it the green pixels can be added diagonally
3.  **Place Azure Diagonally:** If the diagonal is free, place an azure pixel.
4.  **Maintain original:** all original pixels should remain the same
"""

import numpy as np

def find_pixels_by_color(grid, color):
    # Find coordinates of all pixels with the specified color.
    return np.argwhere(grid == color)

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    
    # Find all green pixels.
    green_pixels = find_pixels_by_color(input_grid, 3)
    
    # Iterate through all pairs of green pixels.
    for i in range(len(green_pixels)):
        for j in range(i + 1, len(green_pixels)):
            row1, col1 = green_pixels[i]
            row2, col2 = green_pixels[j]
            
            # Calculate diagonal offsets
            row_diff = row2 - row1
            col_diff = col2 - col1

            # check if a single diagonal exists
            if abs(row_diff) == abs(col_diff) and abs(row_diff) > 0:
              # calculate step for diagonal fill
              row_step = 1 if row_diff > 0 else -1
              col_step = 1 if col_diff > 0 else -1
              
              # find and update the diagonal
              for d in range(1,abs(row_diff)):
                new_row = row1 + d * row_step
                new_col = col1 + d * col_step

                if 0 <= new_row < output_grid.shape[0] and 0 <= new_col < output_grid.shape[1]:
                  output_grid[new_row,new_col] = 8

    return output_grid
```
