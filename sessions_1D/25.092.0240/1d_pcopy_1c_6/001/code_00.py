import numpy as np

"""
Transforms a 1D grid (represented as a list or 1D numpy array) based on the following rule:
Find the single non-white color (C) present in the input grid.
Iterate through the input grid. If a pixel has color C and both its immediate horizontal neighbors are white (0) or grid boundaries, then this pixel is considered "isolated".
For each isolated pixel at index 'i', change the color of the pixels at indices 'i-1' (if valid), 'i', and 'i+1' (if valid) in the output grid to color C.
Pixels that are not isolated non-white pixels, or are white pixels not adjacent to an isolated pixel, retain their original color in the output grid.
"""

def find_non_white_color(grid):
    """Finds the first non-white color in the grid."""
    for pixel in grid:
        if pixel != 0:
            return pixel
    return None # Return None if grid is all white

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list of integers representing the 1D input grid.

    Returns:
        A list of integers representing the transformed 1D output grid.
    """
    # Ensure input is a list or convert numpy array
    if isinstance(input_grid, np.ndarray):
        # Assuming 1D numpy array or a 2D array with one row
        if input_grid.ndim > 1:
           if input_grid.shape[0] == 1:
               input_list = input_grid[0].tolist()
           elif input_grid.shape[1] == 1:
               input_list = input_grid.flatten().tolist()
           else:
                # This case shouldn't happen based on examples, but raise error if it does
                raise ValueError("Input grid has unexpected dimensions for this 1D transformation.")
        else:
             input_list = input_grid.tolist()

    else:
        input_list = list(input_grid) # Make a copy if it's already a list

    width = len(input_list)
    if width == 0:
        return []

    # Initialize output_grid as a copy of the input
    output_grid = list(input_list)

    # Find the non-white color used in this grid
    non_white_color = find_non_white_color(input_list)

    # If no non-white color exists, return the copy directly
    if non_white_color is None:
        return output_grid

    # Iterate through the input grid to find isolated pixels
    for i in range(width):
        # Check if the current pixel has the non-white color
        if input_list[i] == non_white_color:
            # Check if the left neighbor is white or boundary
            left_is_white = (i == 0) or (input_list[i - 1] == 0)

            # Check if the right neighbor is white or boundary
            right_is_white = (i == width - 1) or (input_list[i + 1] == 0)

            # If both neighbors are white (or boundary), it's isolated
            if left_is_white and right_is_white:
                # Modify the output grid: set center pixel
                output_grid[i] = non_white_color
                # Modify the output grid: set left neighbor (if exists)
                if i > 0:
                    output_grid[i - 1] = non_white_color
                # Modify the output grid: set right neighbor (if exists)
                if i < width - 1:
                    output_grid[i + 1] = non_white_color

    return output_grid