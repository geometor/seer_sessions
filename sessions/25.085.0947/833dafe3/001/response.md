```python
"""
Transforms an input grid by creating a larger output grid (double the height and width) 
composed of four quadrants. The bottom-right quadrant is the original input grid. 
The bottom-left quadrant is a horizontal reflection of the input. 
The top-right quadrant is a vertical reflection of the input. 
The top-left quadrant is both a horizontal and vertical reflection of the input.
"""

import numpy as np

def transform(input_grid):
    """
    Applies a reflection tiling transformation to the input grid.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    # Convert the input list of lists to a NumPy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    
    # Determine the height (H) and width (W) of the input grid
    H, W = input_array.shape

    # Create the four quadrants based on reflections of the input array
    
    # Bottom-right: Identity (original input)
    bottom_right = input_array
    
    # Bottom-left: Horizontal flip (flip along the vertical axis, axis=1)
    bottom_left = np.fliplr(input_array)
    
    # Top-right: Vertical flip (flip along the horizontal axis, axis=0)
    top_right = np.flipud(input_array)
    
    # Top-left: Horizontal and Vertical flip (flip along both axes)
    # Can be achieved by flipping top_right horizontally or bottom_left vertically
    top_left = np.fliplr(top_right) # or np.flipud(bottom_left)

    # Assemble the output grid by combining the quadrants
    # Create the top row of quadrants
    top_row = np.concatenate((top_left, top_right), axis=1)
    # Create the bottom row of quadrants
    bottom_row = np.concatenate((bottom_left, bottom_right), axis=1)
    
    # Combine the top and bottom rows
    output_array = np.concatenate((top_row, bottom_row), axis=0)

    # Convert the final NumPy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid

```