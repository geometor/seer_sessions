```python
"""
Transforms a 1D input grid by identifying a single contiguous block of non-white color.
The output grid retains the color of this block only at its starting and ending indices,
with all other pixels set to white (0). If the input is all white, the output is all white.
If the non-white block has length 1, only that single pixel retains its color.
"""

import numpy as np

def transform(input_grid_list):
    """
    Applies the transformation rule to the input grid list.

    Args:
        input_grid_list: A list of integers representing the 1D input grid.

    Returns:
        A list of integers representing the transformed 1D output grid.
    """
    # Convert input list to a numpy array for easier processing
    input_grid = np.array(input_grid_list, dtype=int)
    
    # Get the width (length) of the input grid
    width = input_grid.shape[0]
    
    # Initialize the output grid with the same dimensions, filled with white (0)
    output_grid = np.zeros_like(input_grid)
    
    # Find the indices of all non-white pixels (value != 0)
    non_white_indices = np.where(input_grid != 0)[0]
    
    # Check if any non-white pixels were found
    if non_white_indices.size > 0:
        # Find the index of the first non-white pixel (minimum index)
        first_idx = np.min(non_white_indices)
        
        # Find the index of the last non-white pixel (maximum index)
        last_idx = np.max(non_white_indices)
        
        # Get the color of the non-white segment 
        # (assuming all non-white pixels in the segment have the same color)
        color = input_grid[first_idx]
        
        # Place the color of the first non-white pixel at its original index in the output grid
        output_grid[first_idx] = color
        
        # Place the color of the last non-white pixel at its original index in the output grid
        # This handles the case where first_idx == last_idx correctly.
        output_grid[last_idx] = color
        
    # Convert the output numpy array back to a list before returning
    return output_grid.tolist()

```