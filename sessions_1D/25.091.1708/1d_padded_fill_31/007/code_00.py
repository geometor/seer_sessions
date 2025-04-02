import numpy as np

"""
Processes a 2D grid row by row. For each row containing at least two non-white pixels:
1. Finds the column index of the first (leftmost) non-white pixel ('start_col').
2. Finds the column index of the second non-white pixel ('end_col').
3. Determines the color of the first non-white pixel ('fill_color').
4. Fills the segment in the output grid's row from 'start_col' to 'end_col' (inclusive) with 'fill_color'.
Rows containing fewer than two non-white pixels remain unchanged.
"""

def transform(input_grid):
    """
    Transforms the input grid by filling the segment between the first two
    non-white pixels in each row.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input to numpy array for efficient operations
    input_np = np.array(input_grid, dtype=int)
    # Initialize output grid as a copy of the input
    output_grid = input_np.copy()
    rows, cols = input_np.shape

    # Process each row independently
    for r in range(rows):
        # Find the column indices of all non-white pixels (color != 0) in the current input row
        row_non_white_indices = np.where(input_np[r, :] != 0)[0]

        # Check if the row contains at least two non-white pixels
        if row_non_white_indices.size >= 2:
            # Get the index of the first non-white pixel
            start_col = row_non_white_indices[0]
            # Get the index of the second non-white pixel
            end_col = row_non_white_indices[1]
            # Get the fill color from the first non-white pixel
            fill_color = input_np[r, start_col]

            # Fill the segment in the output grid for the current row
            # The slice `start_col : end_col + 1` includes both start and end columns.
            output_grid[r, start_col : end_col + 1] = fill_color
        # Rows with fewer than two non-white pixels are already correctly copied
        # from the input, so no 'else' block is needed.

    # Return the modified output grid, converted back to list of lists format
    return output_grid.tolist()