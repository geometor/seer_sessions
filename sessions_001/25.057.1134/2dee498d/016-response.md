# 2dee498d • 016 • refine_coder

---
```python
"""
The transformation extracts a variable number of leftmost columns from the input grid to create the output grid. The number of columns to extract is determined by finding the minimal width that contains all unique colors present in the input grid.
"""

import numpy as np

def transform(input_grid):
    # Find the unique colors in the input grid.
    unique_colors = np.unique(input_grid)
    
    # Determine the number of columns to extract.
    num_columns = 0
    found_all_colors = False
    
    for i in range(input_grid.shape[1]):
        num_columns += 1
        current_columns = input_grid[:, :num_columns]
        unique_colors_in_columns = np.unique(current_columns)
        
        # Check if all unique colors are present in the selected columns
        if set(unique_colors) == set(unique_colors_in_columns):
            found_all_colors = True
            break

    # If no columns contain all the colors use the entire grid (should not occur in these ARC examples)
    if not found_all_colors:
      num_columns = input_grid.shape[1]

    # Initialize the output grid.
    output_grid = np.zeros((input_grid.shape[0], num_columns), dtype=int)

    # Copy the determined number of columns from input to output.
    output_grid[:] = input_grid[:, :num_columns]

    return output_grid
```
