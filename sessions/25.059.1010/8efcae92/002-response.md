# 8efcae92 • 002 • example_3 • investigate_coder

---
```python
"""
The transformation rule is as follows:
1. Identify and remove the white (0) background from the input grid.
2. Locate all red (2) pixels within the remaining grid.
3. Find the largest connected component of blue (1) pixels.
4. Create a new, smaller output grid initialized entirely with blue (1).
5. Copy the red (2) pixels from their original positions in the input grid (after background removal) to the corresponding positions in the output grid, preserving their relative positions.
"""

import numpy as np
from scipy.ndimage import label

def get_largest_connected_component(grid, color):
    """
    Finds the largest connected component of a specific color in the grid.
    """
    colored_pixels = (grid == color).astype(int)
    labeled_array, num_features = label(colored_pixels)
    
    if num_features == 0:
        return np.zeros_like(grid)
    
    sizes = np.bincount(labeled_array.ravel())
    largest_label = np.argmax(sizes[1:]) + 1  # +1 because 0 is the background
    largest_component = (labeled_array == largest_label).astype(int)
    return largest_component
    

def transform(input_grid):
    """
    Transforms the input grid by removing the background, finding the
    largest connected component and copying red pixels onto it.
    """
    # Remove background (white pixels)
    non_white_pixels = input_grid[input_grid != 0]

        
    # Find largest blue connected component
    largest_blue = get_largest_connected_component(input_grid, 1)

    # Determine bounding box of the largest blue component
    rows, cols = np.where(largest_blue == 1)
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)

    # Create the output_grid
    output_grid = np.ones((max_row - min_row + 1, max_col - min_col + 1), dtype=int)
    
    #Copy Red pixels into output grid
    for r in range(min_row, max_row+1):
        for c in range(min_col, max_col+1):
            if input_grid[r][c] == 2:
                output_grid[r-min_row][c-min_col] = 2


    return output_grid
```
