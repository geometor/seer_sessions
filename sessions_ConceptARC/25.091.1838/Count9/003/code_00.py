"""
Transform the input grid into a 1-row output grid whose width depends on the count of unique non-background colors in the input.

1. Scan the input grid and identify all the distinct colors present, ignoring the background color (white, value 0).
2. Count how many unique non-background colors were found. Let this count be C.
3. Determine the width N for the output grid. If the count C is exactly 2, set the width N to 3. For any other count C, set the width N to be equal to C.
4. Generate the output grid as a single row (height 1) with N columns, where every cell contains the background color (white, value 0).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid into a single-row output grid based on the count 
    of unique non-background colors.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the output grid (1 row).
    """
    # Convert the input list of lists to a numpy array for efficient processing
    grid_np = np.array(input_grid, dtype=int)

    # Find all unique values in the grid
    unique_values = np.unique(grid_np)

    # Filter out the background color (0) to get only non-background colors
    non_background_colors = unique_values[unique_values != 0]

    # Count the number of unique non-background colors (C)
    count_unique_colors = len(non_background_colors)

    # Determine the width N for the output grid based on the count C
    # If C is 2, N is 3. Otherwise, N is C.
    if count_unique_colors == 2:
        output_width_n = 3
    else:
        output_width_n = count_unique_colors
        
    # Handle the edge case where there are no non-background colors (C=0).
    # In this case, N would be 0, resulting in a 1x0 grid which might be unexpected.
    # Let's assume if C=0, N=0 is intended, leading to an output like [[ ]].
    # If a different output is desired for C=0 (e.g., 1x1 grid [[0]]), adjust here.
    # Based on examples, C is always > 0, so N will be > 0.

    # Create a 1 x N grid filled with the background color (0)
    # Note: np.zeros creates a float array by default, specify dtype=int
    output_grid_np = np.zeros((1, output_width_n), dtype=int)

    # Convert the numpy array back to a list of lists
    output_grid = output_grid_np.tolist()

    return output_grid