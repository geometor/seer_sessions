```python
"""
The transformation rule is to flip the input grid vertically.
Row `i` (0-indexed) of the input grid becomes row `H - 1 - i`
of the output grid, where `H` is the height of the grid. The content
within each row (the order of pixels horizontally) remains unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Flips the input grid vertically.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the vertically flipped grid.
    """
    # Use numpy's flipud function which flips an array in the up/down direction.
    # This directly implements the row mapping described:
    # input_row[0] -> output_row[H-1]
    # input_row[1] -> output_row[H-2]
    # ...
    # input_row[H-1] -> output_row[0]
    output_grid = np.flipud(input_grid)

    return output_grid

```