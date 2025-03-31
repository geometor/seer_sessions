"""
Transforms an input grid by creating a modified version where red (2) pixels are 
changed to azure (8) while keeping white (0) pixels, and then concatenating this 
modified grid horizontally to the left of the original input grid. The final output 
grid has the same height as the input but double the width.
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
    # Convert input list of lists to numpy array if necessary
    input_grid_np = np.array(input_grid, dtype=int)
    
    # Get the dimensions of the input grid
    height, width = input_grid_np.shape

    # 1. Create the transformed_grid by copying the input grid
    transformed_grid = np.copy(input_grid_np)

    # 2. Modify the transformed_grid: change red (2) to azure (8)
    #    Pixels that are red (value 2) in the transformed_grid are set to azure (value 8)
    transformed_grid[transformed_grid == 2] = 8
    #    White pixels (value 0) remain unchanged implicitly as they are not targeted.

    # 3. Create the final output grid with double the width
    #    Initialize with zeros (white)
    output_grid = np.zeros((height, width * 2), dtype=int)

    # 4. Place the transformed_grid into the left half of the output grid
    #    Columns from 0 up to (but not including) width
    output_grid[:, :width] = transformed_grid

    # 5. Place the original input_grid into the right half of the output grid
    #    Columns from width up to the end (2 * width)
    output_grid[:, width:] = input_grid_np

    # 6. Return the final concatenated grid
    return output_grid
