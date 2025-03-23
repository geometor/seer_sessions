```python
"""
The transformation inverts the grid along both its diagonals (main and anti-diagonal).
This is equivalent to performing both a horizontal and a vertical flip.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by flipping it both horizontally and vertically.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert the input grid to a NumPy array for easier manipulation
    input_array = np.array(input_grid)

    # Flip the array horizontally (left to right)
    flipped_horizontal = np.fliplr(input_array)

    # Flip the horizontally flipped array vertically (up to down)
    flipped_both = np.flipud(flipped_horizontal)
    
    # Convert the NumPy array back to a list of lists
    output_grid = flipped_both.tolist()

    return output_grid
```