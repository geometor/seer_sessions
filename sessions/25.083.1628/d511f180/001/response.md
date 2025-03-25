```python
"""
The transformation rule is a global swap of the digits '5' and '8' within the input grid. All other digits remain in their original positions, and the grid dimensions are preserved.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by swapping all occurrences of the digits '5' and '8'.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed grid with '5's and '8's swapped.
    """
    # Convert the input grid to a NumPy array for easier manipulation.
    output_grid = np.array(input_grid)

    # Find all occurrences of '5' and '8'.
    five_indices = np.where(output_grid == 5)
    eight_indices = np.where(output_grid == 8)

    # Swap '5's with '8's and '8' with '5's.
    output_grid[five_indices] = 8
    output_grid[eight_indices] = 5
    

    # Convert the NumPy array back to a list of lists.
    return output_grid.tolist()
```