"""
Identifies isolated non-white pixels in a single-row input grid and expands them
into a horizontal block of three identical pixels in the output grid. An
isolated pixel is defined as a non-white pixel surrounded by white pixels (0)
on its immediate left and right. Existing horizontal blocks of three identical
non-white pixels and background white pixels (unless overwritten by expansion)
are copied directly to the output.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on the expansion rule for isolated pixels.

    Args:
        input_grid (np.ndarray): A 1xN numpy array representing the input grid row.

    Returns:
        np.ndarray: A 1xN numpy array representing the transformed output grid row.
    """
    # Ensure input is a numpy array
    input_grid_np = np.array(input_grid)

    # Create a copy of the input grid to serve as the initial output grid.
    # This handles copying existing blocks and background pixels implicitly.
    output_grid = np.copy(input_grid_np)

    # Get the dimensions (height should be 1, width is the length)
    if input_grid_np.ndim == 1:
      height = 1
      width = input_grid_np.shape[0]
      # Reshape for consistent 2D indexing if it's 1D
      input_grid_np = input_grid_np.reshape(1, -1)
      output_grid = output_grid.reshape(1, -1)
    elif input_grid_np.ndim == 2:
        height, width = input_grid_np.shape
        if height != 1:
            # This specific logic is designed for 1-row grids
            # Handle error or adapt logic if needed for multi-row grids
            raise ValueError("Input grid must have only one row for this transformation.")
    else:
        raise ValueError("Input grid must be 1D or 2D.")


    # Iterate through each pixel of the input grid from index 1 to width-2
    # to allow safe checking of left (i-1) and right (i+1) neighbors.
    for i in range(1, width - 1):
        # Get the color of the current pixel
        current_pixel_color = input_grid_np[0, i]
        # Get the colors of the neighbors
        left_neighbor_color = input_grid_np[0, i - 1]
        right_neighbor_color = input_grid_np[0, i + 1]

        # Check the Expansion Rule conditions:
        # 1. Current pixel is non-white (not 0)
        # 2. Left neighbor is white (0)
        # 3. Right neighbor is white (0)
        if current_pixel_color != 0 and left_neighbor_color == 0 and right_neighbor_color == 0:
            # Apply the expansion: Set the output pixels at indices i-1, i, and i+1
            # to the color of the current pixel.
            output_grid[0, i - 1] = current_pixel_color
            output_grid[0, i] = current_pixel_color
            output_grid[0, i + 1] = current_pixel_color

    # If the original input was 1D, return a 1D array
    if input_grid.ndim == 1:
        return output_grid.flatten()
    else:
        return output_grid
