```python
"""
Finds a 3x3 sub-grid within the input grid that contains only azure (8) and blue (1) pixels and returns it as the output grid.
"""

import numpy as np

def find_target_pattern(input_grid):
    # Iterate through all possible 3x3 sub-grids
    for row in range(input_grid.shape[0] - 2):
        for col in range(input_grid.shape[1] - 2):
            sub_grid = input_grid[row:row+3, col:col+3]
            # Check if the sub-grid contains only azure and blue pixels
            unique_colors = np.unique(sub_grid)
            if np.array_equal(np.sort(unique_colors), np.array([1, 8])):
                return sub_grid
    return None

def transform(input_grid):
    """
    Transforms the input grid to output.
    """
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Find the 3x3 target pattern
    output_grid = find_target_pattern(input_grid)

    return output_grid.tolist()
```