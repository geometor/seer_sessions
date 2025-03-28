```python
"""
Construct the output grid by tiling the input grid and its horizontal flip. 
The output grid has the same height as the input grid and a width five times that of the input grid.
The pattern of tiling is: [original, flipped, original, flipped, original] concatenated horizontally.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by horizontally concatenating the original grid 
    and its horizontal flip in the sequence [O, F, O, F, O].

    Args:
        input_grid (list of lists): The input 2D grid of integers.

    Returns:
        list of lists: The transformed 2D grid.
    """
    # Convert the input list of lists to a NumPy array for easier manipulation
    original_grid = np.array(input_grid, dtype=int)

    # Create a horizontally flipped version of the input grid
    flipped_grid = np.fliplr(original_grid)

    # Define the sequence of grids to concatenate
    sequence = [original_grid, flipped_grid, original_grid, flipped_grid, original_grid]

    # Concatenate the grids horizontally (along axis=1)
    output_grid_np = np.concatenate(sequence, axis=1)

    # Convert the resulting NumPy array back to a list of lists
    output_grid = output_grid_np.tolist()

    return output_grid
```