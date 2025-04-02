import numpy as np

"""
Identifies isolated non-background pixels in a 1xN grid and expands them horizontally.

The transformation rule operates on a 1D array (or a 1xN grid). It scans the array
for a specific pattern: a non-background (non-zero) pixel `C` surrounded by 
background (zero) pixels on both its immediate left and right (`0 C 0`). 
When this pattern is found, the triplet `0 C 0` in the output grid is replaced 
by `C C C`, effectively expanding the isolated pixel into a block of three. 
Pixels not part of this specific pattern are copied directly from the input to 
the output. The scan happens from the second element to the second-to-last 
element to allow checking neighbors.
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the isolated pixel expansion transformation.

    Args:
        input_grid: A 2D numpy array representing the input grid (expected 1xN).

    Returns:
        A 2D numpy array representing the transformed grid.
    """
    
    # Ensure input is a 2D numpy array
    if not isinstance(input_grid, np.ndarray) or input_grid.ndim != 2:
        raise TypeError("Input must be a 2D numpy array.")

    # Based on examples, this task operates on 1xN grids.
    # Add a check or assertion if the transformation is strictly for 1xN grids.
    if input_grid.shape[0] != 1:
         # If not 1xN, the logic might need adjustment or clarification.
         # For now, proceed assuming 1xN based on training examples.
         pass # Or raise ValueError("Input grid must have exactly one row.")

    height, width = input_grid.shape
    
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Iterate through the columns of the grid.
    # We need to check neighbors, so we skip the first (index 0) and 
    # the last (index width-1) columns.
    # The loop range goes up to width-1 (exclusive), so the last index checked is width-2.
    # This ensures input_grid[0, col+1] is always valid.
    for col in range(1, width - 1):
        # Get the color of the current pixel and its immediate horizontal neighbors
        # Since we assume a 1xN grid, the row index is always 0.
        left_pixel_color = input_grid[0, col - 1]
        current_pixel_color = input_grid[0, col]
        right_pixel_color = input_grid[0, col + 1]

        # Check for the pattern: Background - Non-Background - Background (0 C 0 where C != 0)
        if left_pixel_color == 0 and current_pixel_color != 0 and right_pixel_color == 0:
            # If the pattern is found, expand the non-background pixel in the output grid.
            # Change the left, current, and right pixels in the output to the current pixel's color.
            output_grid[0, col - 1] = current_pixel_color
            output_grid[0, col] = current_pixel_color
            output_grid[0, col + 1] = current_pixel_color
            
            # Note: We modify the output_grid, not the input_grid. 
            # The checks in subsequent iterations still use the original input_grid values.

    # Return the modified grid
    return output_grid
