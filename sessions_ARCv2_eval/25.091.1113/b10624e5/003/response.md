```python
"""
Reflects the input grid horizontally across its central vertical axis.
The value of a pixel at coordinate (row, col) in the output grid is 
taken from the value of the pixel at coordinate (row, width - 1 - col) 
in the input grid. The central vertical and horizontal axes (if present) 
are also subject to this reflection rule.
"""

import numpy as np

def transform(input_grid):
    """
    Applies a horizontal reflection to the input grid across its vertical center line.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The horizontally reflected grid.
    """
    # Convert input grid to a numpy array for efficient array manipulation
    grid = np.array(input_grid, dtype=int)
    
    # Get the dimensions of the grid
    # height, width = grid.shape # Not strictly needed for this NumPy approach
    
    # Perform horizontal reflection using NumPy slicing.
    # [:, ::-1] creates a view of the array with all rows (:) 
    # and columns in reverse order (::-1).
    # .copy() is used to create a new array instead of just a view,
    # ensuring the original grid is not modified if it was passed as a numpy array initially.
    output_grid_np = grid[:, ::-1].copy() 
    
    # Convert the resulting numpy array back to a list of lists for the standard ARC format
    output_grid = output_grid_np.tolist()
    
    return output_grid

```