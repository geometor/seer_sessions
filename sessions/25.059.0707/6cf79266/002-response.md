# 6cf79266 • 002 • example_3 • investigate_coder

---
```python
"""
The input grid contains a checkerboard pattern. The background alternates between a color C and 0 (white).
A 3x3 square of color 1 (azure) is inserted into the grid, replacing part of the background pattern
where the background color exists. The location of the azure square is determined by where a 3x3
square could be made using input grid's background. Other cells remain unchanged.
"""

import numpy as np

def find_background_color(grid):
    # Find the most frequent non-zero color, handle edge cases
    unique_colors, counts = np.unique(grid, return_counts=True)
    
    # Exclude 0 (white) when finding the background.
    non_zero_colors = unique_colors[unique_colors != 0]
    non_zero_counts = counts[unique_colors != 0]
    if len(non_zero_colors) > 0 :
       background_color = non_zero_colors[np.argmax(non_zero_counts)]
    else:
        background_color=0 # default when no color.
    return background_color
    

def find_insertion_location(grid, background_color):
    # Find where a 3x3 subgrid can be colored with azure
    height, width = grid.shape
    for r in range(height - 2):
        for c in range(width - 2):
            subgrid = grid[r:r+3, c:c+3]
            if np.all(subgrid == background_color):
                return (r, c)
    return None

def transform(input_grid):
    """
    Transforms the input grid by inserting a 3x3 azure square, replacing the existing background pattern.
    """
    # initialize output_grid
    output_grid = np.copy(input_grid)
    
    # Find the background color
    background_color = find_background_color(input_grid)
    
    # Find an insertion point
    insertion_location = find_insertion_location(input_grid, background_color)

    # change output pixels based on the insertion.
    if insertion_location:
        r, c = insertion_location
        output_grid[r:r+3, c:c+3] = 1

    return output_grid
```
