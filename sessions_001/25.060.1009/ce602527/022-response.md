# ce602527 • 022 • example_4 • investigate_coder

---
```python
"""
The transformation isolates the green object, takes the surrounding blue and green elements, and filters out other colors.
"""

import numpy as np

def find_object(grid, color):
    # Find coordinates of all pixels with the specified color.
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return None  # Object not found
    return coords

def bounding_box(coords):
    # Calculate the bounding box of a set of coordinates.
    min_row = np.min(coords[:, 0])
    max_row = np.max(coords[:, 0])
    min_col = np.min(coords[:, 1])
    max_col = np.max(coords[:, 1])
    return min_row, max_row, min_col, max_col

def extract_region(grid, min_row, max_row, min_col, max_col):
    # Extract a rectangular region from the grid.
    return grid[min_row:max_row+1, min_col:max_col+1]

def filter_colors(grid, allowed_colors):
    # Create a copy of the grid and set disallowed colors to 0 (or another background color).
    filtered_grid = np.copy(grid)
    for color in np.unique(grid):
        if color not in allowed_colors:
            filtered_grid[filtered_grid == color] = 1  # change to the value of blue (1)
    return filtered_grid

def transform(input_grid):
    # Convert input_grid to a NumPy array
    input_grid = np.array(input_grid)

    # 1. Locate the Green Object
    green_coords = find_object(input_grid, 3)

    # 2. Define Bounding Box and Isolate the Region
    min_row, max_row, min_col, max_col = bounding_box(green_coords)

    #Create the bounding box
    output_grid = extract_region(input_grid, min_row-1, max_row+1, min_col-2, max_col+2)

    # 3. Filter Colors
    output_grid = filter_colors(output_grid, [1, 3])
    
    return output_grid.tolist()
```
