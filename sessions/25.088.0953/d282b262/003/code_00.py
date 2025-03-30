import numpy as np

"""
Transformation Rule:
1. Identify all non-white pixels in the input grid. If there are none, return the input grid unchanged.
2. Find the maximum column index (`overall_max_col`) occupied by any non-white pixel across the entire grid.
3. Determine the width of the input grid (`grid_width`).
4. Calculate the single horizontal shift required to move the rightmost pixel to the right edge: `shift = (grid_width - 1) - overall_max_col`.
5. Initialize an output grid of the same dimensions as the input, filled with the background color (white, 0).
6. For each non-white pixel at `(row, col)` with `color` in the input grid:
    a. Calculate its new column position: `new_col = col + shift`.
    b. Place the `color` at `(row, new_col)` in the output grid.
7. Return the completed output grid.
"""

def transform(input_grid):
    """
    Shifts all non-background pixels (considered as a single group) horizontally
    so that the rightmost pixel of the group aligns with the right edge of the grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input list of lists to a NumPy array for easier processing
    input_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape

    # Find coordinates and colors of all non-white pixels
    non_white_pixels = []
    overall_max_col = -1
    for r in range(height):
        for c in range(width):
            color = input_grid_np[r, c]
            if color != 0:
                non_white_pixels.append(((r, c), color))
                overall_max_col = max(overall_max_col, c)

    # Handle edge case: If there are no non-white pixels, return the original grid
    if not non_white_pixels:
        return input_grid

    # Calculate the horizontal shift required
    # shift = target_right_edge - current_overall_right_edge
    shift = (width - 1) - overall_max_col

    # Initialize the output grid with the background color (0)
    output_grid_np = np.zeros_like(input_grid_np)

    # Apply the calculated shift to all non-white pixels and place them on the output grid
    for (r, c), color in non_white_pixels:
        new_c = c + shift
        # Check bounds (although shift calculation should prevent out-of-bounds to the right)
        if 0 <= new_c < width:
            output_grid_np[r, new_c] = color

    # Convert the output NumPy array back to a list of lists
    output_grid = output_grid_np.tolist()

    return output_grid