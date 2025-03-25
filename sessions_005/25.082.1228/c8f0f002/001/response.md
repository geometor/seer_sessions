```python
"""
Replaces all instances of color 7 (orange) in the input grid with color 5 (gray).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by replacing all occurrences of color 7 with color 5.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed grid.
    """
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Find all occurrences of color 7 and replace them with color 5.
    output_grid[output_grid == 7] = 5

    return output_grid
```