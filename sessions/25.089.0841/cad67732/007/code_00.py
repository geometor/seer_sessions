import numpy as np

"""
Transforms the input grid by creating a new grid with double the height and double the width of the input grid.
The input grid is copied into the top-left quadrant of the new grid.
An identical copy of the input grid is also placed into the bottom-right quadrant of the new grid.
The remaining quadrants (top-right and bottom-left) are filled with the background color, which is assumed to be 0 (white) based on the examples.
"""

def transform(input_grid):
    """
    Creates an output grid double the dimensions of the input grid,
    placing two copies of the input grid diagonally (top-left and bottom-right)
    and filling the remaining quadrants with the background color (0).

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed grid.
    """
    # Convert input list of lists to a NumPy array for efficient slicing
    input_np = np.array(input_grid, dtype=int)

    # Determine the height (H) and width (W) of the input grid.
    H, W = input_np.shape

    # Calculate the dimensions of the output grid (double the input).
    output_height = 2 * H
    output_width = 2 * W

    # Create a new output grid initialized with the background color (0).
    # Using np.zeros ensures the background is filled correctly.
    output_grid_np = np.zeros((output_height, output_width), dtype=int)

    # Copy the input grid into the top-left quadrant of the output grid.
    # The slice [0:H, 0:W] refers to rows 0 to H-1 and columns 0 to W-1.
    output_grid_np[0:H, 0:W] = input_np

    # Copy the input grid again into the bottom-right quadrant of the output grid.
    # The slice [H:output_height, W:output_width] refers to rows H to 2H-1
    # and columns W to 2W-1.
    output_grid_np[H:output_height, W:output_width] = input_np

    # Convert the NumPy array back to a list of lists for the final output.
    return output_grid_np.tolist()
