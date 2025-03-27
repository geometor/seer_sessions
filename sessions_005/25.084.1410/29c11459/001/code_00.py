import numpy as np

"""
Identify the row containing exactly two non-white pixels, one at the far left (column 0) 
and one at the far right (column 10). Fill the gap between these two pixels in that row. 
The fill uses the color of the left pixel for the left half of the gap (columns 1-4) 
and the color of the right pixel for the right half of the gap (columns 6-9). 
The exact midpoint column (column 5) is filled with gray (5). 
All other pixels remain unchanged.
"""

def transform(input_grid):
    """
    Transforms the input grid by filling a horizontal gap between two boundary pixels.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # Define expected positions and midpoint based on examples (width=11)
    left_col = 0
    right_col = width - 1 # 10 for width 11
    mid_col = (width - 1) // 2 # 5 for width 11
    midpoint_color = 5 # Gray

    # Iterate through each row to find the target row
    for r in range(height):
        # Check if the row matches the pattern: non-white at ends, white in between
        is_target_row = (
            input_grid[r, left_col] != 0 and
            input_grid[r, right_col] != 0 and
            np.all(input_grid[r, left_col + 1 : right_col] == 0) # Check if middle is all white
        )

        if is_target_row:
            # Get the colors from the boundary pixels
            left_color = input_grid[r, left_col]
            right_color = input_grid[r, right_col]

            # Fill the left part of the gap in the output grid
            # Columns from left_col + 1 up to (but not including) mid_col
            output_grid[r, left_col + 1 : mid_col] = left_color

            # Fill the right part of the gap in the output grid
            # Columns from mid_col + 1 up to (but not including) right_col
            output_grid[r, mid_col + 1 : right_col] = right_color

            # Fill the midpoint pixel
            output_grid[r, mid_col] = midpoint_color

            # Assuming only one such row needs modification based on examples
            break

    return output_grid