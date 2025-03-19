# dc433765 • 014 • refine_coder

---
```python
"""
Moves all pixels of a specific color one position to the right. The color to move is determined as the non-background color that appears at the bottom-right corner of the input grid.
"""

import numpy as np

def get_target_color(input_grid):
    """Determines the target color to be moved."""
    # Get the dimensions of the input grid
    rows, cols = input_grid.shape
    # Get color at bottom right corner
    target_color = input_grid[rows - 1, cols - 1]
    
    # Determine background color (most frequent)
    vals, counts = np.unique(input_grid, return_counts=True)
    background_color = vals[np.argmax(counts)]    
    
    # Return target color if not background
    if target_color != background_color:
        return target_color
    else:
        return None #no target color

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    #get target color
    target_color = get_target_color(input_grid)
    
    if target_color is None:
        return output_grid
    
    # Determine background color
    vals, counts = np.unique(input_grid, return_counts=True)
    background_color = vals[np.argmax(counts)]

    # Iterate through the grid and move target color pixels
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == target_color:
                output_grid[r, c] = background_color  # Set original position to background
                new_c = min(cols - 1, c + 1)          # Move one position to the right (within bounds)
                output_grid[r, new_c] = target_color  # Set new position to target color

    return output_grid
```
