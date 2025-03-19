# c8cbb738 • 008 • refine_coder

---
```python
"""
The transformation rule identifies largest contiguous block of non-green pixels in the input grid. 
The output grid is just this shape, and the colors are preserved. 
If the entire image is filled with the largest object, besides green, then the output is just [3]
"""

import numpy as np

def get_largest_object(grid):
    # Count each color
    unique, counts = np.unique(grid, return_counts=True)
    color_counts = dict(zip(unique, counts))
    
    # Find color with largest count, excluding green
    largest_color = None
    largest_count = 0
    for color, count in color_counts.items():
        if color != 3 and count > largest_count:
            largest_count = count
            largest_color = color
    
    if largest_color is None:
        return None, 0, 0, []
    
    # Find contiguous pixels of largest color
    mask = (grid == largest_color).astype(int)
    
    
    # Get dimensions of largest color
    coords = np.argwhere(mask)
    
    # Check if the entire image is filled with the largest object
    if len(coords) == (grid.shape[0] * grid.shape[1]):
        return largest_color, 0, 0, [] #special flag

    #calculate width and height
    width = np.max(coords[:, 1]) - np.min(coords[:, 1]) + 1
    height = np.max(coords[:, 0]) - np.min(coords[:, 0]) + 1

    return largest_color, width, height, coords

def transform(input_grid):
    # Convert input grid to a NumPy array
    input_grid = np.array(input_grid)

    # Get the largest non-green object
    largest_color, width, height, coords = get_largest_object(input_grid)

    # Handle edge case where the entire image is filled.
    if largest_color is not None and width == 0 and height == 0:
        return [[3]]

    # If no non-green object is found, return original grid shape with green.
    if largest_color is None:
        return input_grid.tolist() # Should never occur

    #create output
    min_row = np.min(coords[:, 0])
    min_col = np.min(coords[:, 1])
    output_grid = input_grid[min_row:min_row+height, min_col:min_col+width]

    return output_grid.tolist()
```
