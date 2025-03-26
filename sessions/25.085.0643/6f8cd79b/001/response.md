```python
"""
Create an output grid of the same dimensions as the input grid.
Iterate through each cell of the grid. 
If the cell is located on the border (first or last row, or first or last column), 
set its color to azure (8) in the output grid.
Otherwise (if the cell is in the interior), set its color in the output grid 
to its original color from the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Applies a border of azure (8) to the input grid.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the output grid with an azure border.
    """
    # Convert input list of lists to numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    
    # Get the dimensions of the input grid
    height, width = input_grid_np.shape
    
    # Initialize output_grid as a copy of the input_grid
    # This handles preserving the interior pixels correctly.
    output_grid = np.copy(input_grid_np)
    
    # Define the border color
    border_color = 8 # azure

    # Change border pixels in the output grid
    
    # Set the top row to border_color
    if height > 0:
        output_grid[0, :] = border_color
        
    # Set the bottom row to border_color
    if height > 1: # Avoid setting row 0 twice for 1-row grids
        output_grid[height - 1, :] = border_color
        
    # Set the first column to border_color
    if width > 0:
        output_grid[:, 0] = border_color
        
    # Set the last column to border_color
    if width > 1: # Avoid setting col 0 twice for 1-column grids
        output_grid[:, width - 1] = border_color

    # Convert back to list of lists if required by the environment,
    # otherwise return the numpy array. Assuming numpy array is acceptable.
    return output_grid.tolist() # Or just return output_grid if numpy is okay

```