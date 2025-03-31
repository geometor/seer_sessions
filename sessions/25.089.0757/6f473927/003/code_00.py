"""
Transforms an input grid by creating a modified version where red (2) pixels are 
changed to azure (8), and then concatenating this modified grid horizontally to 
the left of the original input grid. The final output grid has the same height 
as the input but double the width.
"""

import numpy as np

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    # Convert input list of lists to numpy array if it's not already one
    # Ensure the dtype is integer
    input_grid_np = np.array(input_grid, dtype=int)
    
    # 1. Determine the height (H) and width (W) of the input grid.
    height, width = input_grid_np.shape

    # 2. Create a new grid, called `modified_grid`, by making a copy of the input grid.
    modified_grid = np.copy(input_grid_np)

    # 3. Iterate through each pixel of the `modified_grid`. If a pixel's color is red (2), 
    #    change its color to azure (8). Leave all other pixel colors unchanged.
    #    This is done efficiently using numpy boolean indexing.
    modified_grid[modified_grid == 2] = 8

    # 4. Create the final output grid with height H and width (2 * W), 
    #    initialized with a default color (e.g., white 0).
    #    Numpy initializes with zeros by default if dtype is specified.
    output_grid = np.zeros((height, width * 2), dtype=int)

    # 5. Copy the `modified_grid` into the left half of the output grid 
    #    (columns 0 to W-1).
    output_grid[:, :width] = modified_grid

    # 6. Copy the original `input_grid` into the right half of the output grid 
    #    (columns W to 2*W-1).
    output_grid[:, width:] = input_grid_np

    # 7. Return the final output grid.
    return output_grid