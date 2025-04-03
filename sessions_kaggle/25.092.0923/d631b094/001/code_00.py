"""
Extract all non-white pixels from the input grid and arrange them horizontally in a single row in the output grid, preserving the order they appear in when scanning the input grid top-to-bottom, left-to-right.
"""

import numpy as np

def transform(input_grid):
    """
    Extracts non-white pixels from the input grid and arranges them in a single row.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        numpy.ndarray: A 1D numpy array (single row) containing the non-white pixels
                       in the order they were found (top-to-bottom, left-to-right).
    """
    # Convert input list of lists to a numpy array for easier iteration
    grid = np.array(input_grid, dtype=int)

    # 1. Create an empty list to store the colors of the non-white pixels found.
    non_white_pixels = []

    # 2. Iterate through each row of the input grid from the top row to the bottom row.
    rows, cols = grid.shape
    for r in range(rows):
        # 3. For each row, iterate through each cell (pixel) from the left column to the right column.
        for c in range(cols):
            pixel_color = grid[r, c]
            # 4. Check the color of the current pixel. If the color is not white (i.e., the value is not 0),
            #    add this color value to the end of the list.
            if pixel_color != 0:
                non_white_pixels.append(pixel_color)

    # 5. After scanning the entire input grid, create a new output grid that has 1 row
    #    and a number of columns equal to the total number of color values collected in the list.
    # 6. Populate the single row of the output grid using the color values from the list,
    #    in the same order they were added to the list.
    # Note: Numpy arrays are used, so a 1D array represents the single row.
    output_grid = np.array(non_white_pixels, dtype=int)

    # Reshape into a 2D array with 1 row if needed by the framework,
    # otherwise return the 1D array directly if that's acceptable.
    # For ARC tasks, the output is expected as a grid (2D array).
    if output_grid.size > 0:
        output_grid = output_grid.reshape(1, -1)
    else:
        # Handle the case where there are no non-white pixels
        output_grid = np.array([[]], dtype=int) # Empty 1x0 grid


    return output_grid