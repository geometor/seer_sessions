"""
Combines two subgrids from the input grid based on a pixel-wise OR logic.

1. Identifies a horizontal separator line of yellow (4) pixels.
2. Extracts the subgrid above the separator (top_grid) and the subgrid below it (bottom_grid).
3. Creates an output grid with the same dimensions as the top/bottom subgrids.
4. Iterates through each pixel position (r, c).
5. If the pixel at top_grid[r][c] is blue (1) OR the pixel at bottom_grid[r][c] is red (2), the corresponding output_grid[r][c] is set to green (3).
6. Otherwise (if both input pixels are white (0)), the output_grid[r][c] remains white (0).
"""

import numpy as np

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    input_grid = np.array(input_grid)
    height, width = input_grid.shape

    # Find the yellow separator row
    separator_row_index = -1
    for r in range(height):
        if np.all(input_grid[r, :] == 4):
            separator_row_index = r
            break

    if separator_row_index == -1:
        # Handle cases where the separator might be missing (though unlikely based on examples)
        # For now, let's assume it's always present as per the observed pattern.
        # Or raise an error: raise ValueError("Separator row not found")
        # Based on the examples, the separator always exists.
        pass 

    # Extract the top and bottom subgrids
    top_grid = input_grid[:separator_row_index, :]
    bottom_grid = input_grid[separator_row_index + 1:, :]

    # Get dimensions for the output grid (should match top/bottom grid)
    output_height, output_width = top_grid.shape

    # Initialize the output grid with white (0)
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through each pixel position and apply the combination logic
    for r in range(output_height):
        for c in range(output_width):
            # Check if the pixel in the top grid is blue (1)
            is_top_blue = top_grid[r, c] == 1
            # Check if the pixel in the bottom grid is red (2)
            is_bottom_red = bottom_grid[r, c] == 2

            # Apply the OR logic: if either is colored, output is green (3)
            if is_top_blue or is_bottom_red:
                output_grid[r, c] = 3
            # Otherwise, it remains white (0) as initialized

    return output_grid.tolist() # Return as list of lists per ARC standard