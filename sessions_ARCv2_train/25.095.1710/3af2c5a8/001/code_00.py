"""
Transforms an input grid by creating a larger output grid (2x height, 2x width) 
composed of four quadrants. The top-left quadrant is the original input grid. 
The top-right quadrant is the input grid flipped horizontally. 
The bottom-left quadrant is the input grid flipped vertically. 
The bottom-right quadrant is the input grid flipped both horizontally and vertically.
"""

import numpy as np

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies a 2x2 tiling transformation to the input grid using flips.

    Args:
        input_grid: A list of lists representing the input 2D integer grid.

    Returns:
        A list of lists representing the transformed 2D integer grid, which is
        twice the height and twice the width of the input grid.
    """
    # Convert input list of lists to a NumPy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)

    # Get the dimensions of the input grid
    rows, cols = input_np.shape

    # Calculate the dimensions of the output grid
    output_rows = rows * 2
    output_cols = cols * 2

    # Initialize the output grid with zeros (or any placeholder)
    output_np = np.zeros((output_rows, output_cols), dtype=int)

    # Perform transformations and place them into the corresponding quadrants

    # Top-Left Quadrant: Original input grid
    output_np[0:rows, 0:cols] = input_np

    # Top-Right Quadrant: Horizontally flipped input grid
    output_np[0:rows, cols:output_cols] = np.fliplr(input_np)

    # Bottom-Left Quadrant: Vertically flipped input grid
    output_np[rows:output_rows, 0:cols] = np.flipud(input_np)

    # Bottom-Right Quadrant: Flipped horizontally and vertically
    output_np[rows:output_rows, cols:output_cols] = np.flipud(np.fliplr(input_np))
    # Alternatively: output_np[rows:output_rows, cols:output_cols] = np.rot90(input_np, 2) # Rotate 180 degrees

    # Convert the resulting NumPy array back to a list of lists
    output_grid = output_np.tolist()

    return output_grid
