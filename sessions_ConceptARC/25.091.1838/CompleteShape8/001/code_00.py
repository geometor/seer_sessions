"""
Transform the input grid by performing the following steps:
1. Create a new output grid of the same dimensions as the input, filled with the background color (white, 0).
2. Identify all unique colors present in the input grid, excluding white (0) and gray (5).
3. For each identified unique color:
    a. Find the coordinates of all pixels in the input grid that have this color.
    b. Calculate the minimum and maximum row and column indices for these pixels to determine their bounding box.
    c. Fill the rectangular area defined by this bounding box in the output grid with the current color.
4. Return the resulting output grid. Gray objects (color 5) in the input are ignored.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the bounding box filling transformation to the input grid.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # Get input grid dimensions
    height, width = input_grid.shape

    # Initialize output_grid with the same dimensions, filled with white (0)
    output_grid = np.zeros((height, width), dtype=int)

    # Find unique colors in the input grid, excluding white (0) and gray (5)
    unique_colors = np.unique(input_grid)
    colors_to_process = [c for c in unique_colors if c != 0 and c != 5]

    # Process each relevant color
    for color in colors_to_process:
        # Find coordinates of pixels with the current color
        rows, cols = np.where(input_grid == color)

        # Check if any pixels of this color were found
        if rows.size > 0:
            # Calculate the bounding box
            min_r, max_r = np.min(rows), np.max(rows)
            min_c, max_c = np.min(cols), np.max(cols)

            # Fill the bounding box area in the output grid with the current color
            # Note: Slicing is inclusive of the start index and exclusive of the end index,
            # so we add 1 to the max indices.
            output_grid[min_r : max_r + 1, min_c : max_c + 1] = color

    return output_grid
