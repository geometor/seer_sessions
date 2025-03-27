```python
"""
1. Iterate through each row of the input grid.
2. Identify rows which are composed of a single color that spans the complete width of the grid
3. Extract the unique colors from those rows
4. For each extracted unique color, create a new row in the output grid.
5. Each row of output grid should contains the unique color repeated four times.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid into a summarized output grid based on full-width rows.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the output grid.
    """
    output_grid = []

    # Iterate through each row of the input grid
    for row in input_grid:
        unique_colors = np.unique(row)

        # Check if the row consists of a single color
        if len(unique_colors) == 1:
            color = unique_colors[0]

            # Create a new row in the output grid with the color repeated four times
            output_row = [color] * 4
            output_grid.append(output_row)

    return np.array(output_grid)
```