# 4be741c5 • 002 • example_3 • investigate_coder

---
```python
"""
The transformation rule identifies the unique colors present in the input grid and creates a 1-dimensional output grid. The output grid contains each unique color once, maintaining the order in which the colors first appear in the input grid when scanning from top to bottom and left to right.
"""

import numpy as np

def get_unique_colors_ordered(input_grid):
    """
    Extracts unique colors from the input grid in order of appearance.
    """
    unique_colors = []
    for row in input_grid:
        for pixel in row:
            if pixel not in unique_colors:
                unique_colors.append(pixel)
    return unique_colors

def transform(input_grid):
    """
    Transforms an input grid into a 1D grid of unique colors, maintaining order of appearance.
    """
    # Convert input_grid to numpy array for easier manipulation.
    input_grid = np.array(input_grid)

    # Get unique colors in order of appearance.
    unique_colors = get_unique_colors_ordered(input_grid)
    
    # Determine output grid dimensions based on the first example.
    # Assuming if colors tend to span horizontally, make output horizontal as well.
    if input_grid.shape[1] > input_grid.shape[0] :
      output_grid = np.array(unique_colors).reshape(1,-1)
    else:
      output_grid = np.array(unique_colors).reshape(-1,1)
    

    return output_grid.tolist()
```
